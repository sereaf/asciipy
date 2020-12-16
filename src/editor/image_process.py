import math
import random
import os
import colorsys
from PIL import ImageDraw, Image, ImageOps
import cv2
import numpy as np

""" 
	Image processing functions to turn pixels / images to ascii
"""

def save_img(output, to, img, img_out, pillow=False):
	"""
		Save image with right name and extension
	"""
	if to:
		ext = to
	else:
		ext = '.jpg'

	if os.path.exists(img) and to == False:
		path = img
		ext = os.path.splitext(name)[1]
	try:
		cv2.imwrite(output + ext, img_out)
	except:
		raise ValueError('Can\'t save image - %s' % (output + ext))

def getChars(chars, density_flip=False):
	""" 
		Get char list, len and interval from a string of chars 
	"""
	charArray = list(chars)
	charLength = len(charArray)
	interval  = charLength / 256

	if density_flip:
		charArray = charArray[::-1]

	return charArray, charLength, interval

def getChar(inputInt, charArray, interval):
	""" 
		Get the right character from a list of characters
	"""
	return charArray[math.floor(inputInt * interval)]

def pixel_density(pixel):
	b, g, r = pixel
	return (0.2126 * r + 0.7152 * g + 0.0722 * b) 

def create_blank(width, height, bgr_color=(0, 0, 0)):
	"""
	Create new image (numpy array) filled with certain color in RGB pixels
	"""
	image = np.zeros((height, width, 3), np.uint8)
	image[:] = bgr_color
	return image

def color_reverse(color):
	""" 
	Convert bgr pixel to rgb and vice versa
	"""
	color = tuple(reversed(color))

def rgb_to_ansi(rgb_color):
	"""
	Convert an rgb color to ansi color
	"""
	r , g, b = rgb_color
	if r == g & g == b:
		if r < 8:
			return int(16)
		if r > 248:
			return int(230)
		return int(round(((r - 8) / 247) * 24) + 232)

	r_in_range = get_ansi_range(r)
	g_in_range = get_ansi_range(g)
	b_in_range = get_ansi_range(b)
	ansi = 16 + (36 * r_in_range) + (6 * g_in_range) + b_in_range
	return int(ansi)

get_ansi_range = lambda a: int(round(a / 51.0))

def pil_to_cv2(pil_img):
	""" 
		Convert pillow image to opencv image
	"""
	open_cv_image = np.array(pil_img.convert('RGB'))
	return open_cv_image[:, :, ::-1].copy()
	#return np.array(pil_img)

def cv2_to_pil(cv2_img):
	""" 
		Convert opencv image to pillow image
	"""
	color_converted = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
	return Image.fromarray(color_converted)

def create_ascii_img(size, img, img_out, char, font, option, font_scale=1, pillow=False):
	"""
	Creates the ascii image - get the right characters and puts it onto the image
	Converts from pillow to opencv or from opencv to pillow image if needed
	"""
	bandw = False
	if option == 'bandw' or option == 'filled-bandw' or option == '2char-bandw' or option == 'full-filled-bandw':
		bandw = True
		if pillow:
			img = ImageOps.grayscale(img)
		else:	
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	if pillow:
		img = img.load()
		draw = ImageDraw.Draw(img_out)
	w, h = size
	for i in range(h):
		for j in range(w):
			if pillow:
				if bandw:
					b, g, r = img[j, i], img[j, i], img[j, i]
				else:
					r, g, b = img[j, i] # rgb
				color = (int(r), int(g), int(b))
			else:
				if bandw:
					b, g, r = img[i][j], img[i][j], img[i][j]
				else:
					b, g, r = img[i, j] # bgr
				color = (int(b), int(g), int(r))
			density = pixel_density(color)
			if pillow:
				draw.text((j * char[2], i * char[3]), getChar(density, char[0], char[1]), font = font, fill = color)
			else:
				cv2.putText(img_out, getChar(density, char[0], char[1]), (j * char[2], (i + 1) * char[3]), int(font),  font_scale, color)
	if pillow:
		return pil_to_cv2(img_out) 
	return img_out


class TerminalColorMapException(Exception):
    pass


def _rgb(color):
    return ((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff)


def _diff(color1, color2):
    (r1, g1, b1) = _rgb(color1)
    (r2, g2, b2) = _rgb(color2)
    return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)


class TerminalColorMap:

    def getColors(self, order='rgb'):
        return self.colors

    def convert(self, hexcolor):
        diffs = {}
        for xterm, rgb in self.colors.items():
            diffs[_diff(rgb, hexcolor)] = xterm
        minDiffAnsi = diffs[min(diffs.keys())]
        return (minDiffAnsi, self.colors[minDiffAnsi])

    def colorize(self, string, rgb=None, ansi=None, bg=None, ansi_bg=None):
        '''Returns the colored string'''
        if not isinstance(string, str):
            string = str(string)
        if rgb is None and ansi is None:
            raise TerminalColorMapException(
                'colorize: must specify one named parameter: rgb or ansi')
        if rgb is not None and ansi is not None:
            raise TerminalColorMapException(
                'colorize: must specify only one named parameter: rgb or ansi')
        if bg is not None and ansi_bg is not None:
            raise TerminalColorMapException(
                'colorize: must specify only one named parameter: bg or ansi_bg')

        if rgb is not None:
            (closestAnsi, closestRgb) = self.convert(rgb)
        elif ansi is not None:
            (closestAnsi, closestRgb) = (ansi, self.colors[ansi])

        if bg is None and ansi_bg is None:
            return "\033[38;5;{ansiCode:d}m{string:s}\033[0m".format(ansiCode=closestAnsi, string=string)

        if bg is not None:
            (closestBgAnsi, unused) = self.convert(bg)
        elif ansi_bg is not None:
            (closestBgAnsi, unused) = (ansi_bg, self.colors[ansi_bg])

        return "\033[38;5;{ansiCode:d}m\033[48;5;{bf:d}m{string:s}\033[0m".format(ansiCode=closestAnsi, bf=closestBgAnsi, string=string)


class VT100ColorMap(TerminalColorMap):
    primary = [
        0x000000, 0x800000, 0x008000, 0x808000, 0x000080, 0x800080, 0x008080, 0xc0c0c0
    ]

    bright = [
        0x808080, 0xff0000, 0x00ff00, 0xffff00, 0x0000ff, 0xff00ff, 0x00ffff, 0xffffff
    ]

    def __init__(self):
        self.colors = dict()
        self._compute()

    def _compute(self):
        for index, color in enumerate(self.primary + self.bright):
            self.colors[index] = color


class XTermColorMap(VT100ColorMap):
    grayscale_start = 0x08
    grayscale_end = 0xf8
    grayscale_step = 10
    intensities = [
        0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF
    ]

    def _compute(self):
        for index, color in enumerate(self.primary + self.bright):
            self.colors[index] = color

        c = 16
        for i in self.intensities:
            color = i << 16
            for j in self.intensities:
                color &= ~(0xff << 8)
                color |= j << 8
                for k in self.intensities:
                    color &= ~0xff
                    color |= k
                    self.colors[c] = color
                    c += 1

        c = 232
        for hex in list(range(self.grayscale_start, self.grayscale_end, self.grayscale_step)):
            color = (hex << 16) | (hex << 8) | hex
            self.colors[c] = color
            c += 1


def get_ansi(string, ansi_color):
    a = XTermColorMap()
    return a.colorize(string=string, ansi=ansi_color)

def get_charset(chars, option):
	all_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~i!lI;:,\"^`. "
	filled_chars = "▓▒░█"
	f_filled_chars = "█"
	_2char = "█ "
	if chars == None:
			if option == 'colored' or option == 'bandw':
				return all_chars
			elif option == 'filled' or option == 'filled-bandw':
				return filled_chars
			elif option == 'full-filled' or option == 'full-filled-bandw':
				return f_filled_chars		
			elif option =='2char' or option == '2char-bandw':
				return _2char
			else:
				return all_chars
	else:
		return chars

def scale_to_float(scale):
	try:
		scale = float(scale)
	except:
		pass
	return scale

def increase_saturation(r, g, b):
    """
    Increase the saturation from rgb and return the new value as rgb tuple
    """
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    s = min(s+0.3, 1.0)
    return colorsys.hsv_to_rgb(h, s, v)