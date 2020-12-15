import os
import math
import cv2
import sys
from PIL import ImageOps, Image
import numpy as np
from to_ascii.font import InputFont
from to_ascii.utils import *
from to_ascii.image_process import *

class ImageForAscii:
	def __init__(self, imgIn):
		self.pathIn = imgIn
		self.image = None
		#self.load()

	def load(self, pillow=False):
		"""
		Load the image correctly
		"""
		if os.path.exists(str(self.pathIn)):
			if pillow:
				self.image = Image.open(self.pathIn)
			else:
				self.image = cv2.imread(self.pathIn)
		elif type(self.pathIn) is list or type(self.pathIn).__module__ == np.__name__:
			if pillow:
				self.image = cv2_to_pil(self.pathIn)
			else:
				self.image = self.pathIn
		else:
			raise ValueError('Can\'t load image')
	
	def get(self):
		return self.image

	def get_shape(self, pillow=False):
		"""
		Get the width and height of the image
		"""
		if pillow:
			return self.image.size
		else:
			# reversed - cv2 returns (height, width)
			return self.image.shape[:2][::-1]

	def resize(self, size, pillow=False):
		"""
		Resize the image
		"""
		w, h = size
		if pillow:
			i = self.image.resize((w, h), Image.NEAREST)
		else:
			i = cv2.UMat(cv2.resize(self.image, (w, h), interpolation = cv2.INTER_CUBIC)).get()
		return i, w, h
		
	def remove(self):
		os.remove(self.pathIn)

	@timeit
	def ascii_img(self, output='', action='save', option='colored', font=2, save_as='', scale='fit', density_flip=False, character_space='', chars=None, font_scale=1):
		"Create an ascii image"
		load_fnt = InputFont(font, font_scale)
		font = load_fnt.font
		pillow = load_fnt.custom_font
		self.load(pillow)
		chars = get_charset(chars, option)

		# get space between characters 
		if character_space == '':
			oneCharWidth, oneCharHeight = load_fnt.get_size('#')
		elif character_space == 'avg':
			oneCharWidth, oneCharHeight = load_fnt.get_avg_size(chars)
		elif character_space == 'sm':
			oneCharWidth, oneCharHeight = load_fnt.get_smallest_size(chars)
		elif character_space == 'bg':
			oneCharWidth, oneCharHeight = load_fnt.get_biggest_size(chars)

		size = self.get_shape(pillow)

		scale = scale_to_float(scale)

		if scale == 'fit':
			new_size = (round(size[0] / oneCharWidth), round(size[1] / oneCharHeight))
		else:
			new_size = int(scale * size[0]), int(scale * size[1] * (oneCharWidth / oneCharHeight))

		redized_img, width, height = self.resize(new_size, pillow)

		if pillow:
			img_out = Image.new('RGB', (size[0], size[1]), color = (0, 0, 0))
		else:
			img_out = create_blank(size[0], size[1])

		charArray, charLength, interval = getChars(chars, density_flip)
		img_out = create_ascii_img((width, height), redized_img, img_out, [charArray, interval, oneCharWidth, oneCharHeight], font, option, font_scale, pillow)
		if action == 'save':
			output = get_path_out(self.pathIn, output)
			save_img(output, save_as, self.pathIn, img_out, pillow)
		elif action == 'return':
			return img_out
		elif action == 'show':	
			cv2.imshow('ascii_img', img_out)
			cv2.waitKey(0)
			cv2.destroyAllWindows() 

	#BOLD = '\033[1m'
	def ascii_terminal(self, option='colored', action='play', scale='fit', terminal_size=None, density_flip=False, chars=None, ratio_to='width', character_space='', terminal_spacing=None, clear=False):
		"""
		Create & print ascii image to terminal
		"""
		self.load()
		size = self.get_shape()
		if terminal_size is None:
			try:
				terminal_width, terminal_height = os.get_terminal_size()
			except:
				terminal_width, terminal_height = (53, 30)
		else:
			terminal_width, terminal_height = terminal_size

		# fit the terminal width to the terminal height or vice versa 
		if ratio_to in 'width':
			ratio = float(size[0] / size[1])
			terminal_width = round(terminal_height * ratio)
		elif ratio_to in 'height':
			ratio = float(size[1] / size[0])
			terminal_height = round(terminal_width * ratio)
		else: # if ratio=pass or something else - defalult terminal size 
			pass

		chars = get_charset(chars, option)

		scale = scale_to_float(scale)

		if scale == 'fit':
			new_size = terminal_width, terminal_height
		else:
			new_size = int(scale * size[0]), int(scale * size[1])

		img, width, height = self.resize(new_size)
		charArray, charLength, interval = getChars(chars, density_flip)
		bandw = False
		if option == 'bandw' or option == 'filled-bandw' or option == '2char-bandw' or option == 'full-filled-bandw':
			bandw = True	
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		ascii_chars_list = [] 
		os.system('')
		for i in range(height):
			for j in range(width):
				if bandw:
					b, g, r = img[i][j], img[i][j], img[i][j]
				else:
					b, g, r = img[i, j] # bgr
				# turn pixels into a character and an ansi value
				color = (int(r), int(g), int(b))
				ansi_color = rgb_to_ansi(color)
				density = pixel_density(color)
				char =  getChar(density, charArray, interval) * 2
				ansi = get_ansi(char, ansi_color)
				ascii_chars_list.append(ansi)

		
		if action == 'play' or action == 'save':
			print_terminal(ascii_chars_list, (terminal_width, terminal_height), terminal_spacing, clear)
			return 
		elif action == 'return':
			return ascii_chars_list, terminal_width, terminal_height
		else:
			pass



	""" rgb = increase_saturation(r, g, b)
		print('\033[38;5;%s;%s;%sm a %s' % (r, g, b, '\033[0m'))
		ansi = f'\033[38;5;{r};{g};{b}m{char}\033[0m'	
		print("\033[A{}\033[A".format(''.join(['']*(terminal_width * terminal_height))))
		sys.stdout.write("\033[F")
		print("\033[A{}\033[A".format(''.join([' ']*(terminal_width * terminal_height))))
		with open('txt.txt', 'a+') as a:
			for i in range(len(_all)):
				if i % terminal_width == 0:
					a.write(_all[i] + '\r\n')
				else:
					a.write(_all[i]) """
