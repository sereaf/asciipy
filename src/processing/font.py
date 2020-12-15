import cv2
from PIL import ImageFont
import os
import numpy as np

""" 
 This module contains methods to determine how to put the characters with correct font onto images 
"""

class InputFont:
	
	def __init__(self, font, font_scale, thickness=1):
		self.font = font
		self.font_scale = font_scale
		self.thickness = thickness
		self.custom_font = False
		self.avg_size = None
		self.smallest_size = None
		self.biggest_size = None
		self.get_type()

	def get_type(self):
		""" 
		is built in cv2 font or custom - (load with pillow if custom) - load it
		"""
		try:
			self.font = int(self.font)
		except:
			ext = os.path.splitext(os.path.basename(self.font))[1]
			if ext == '.pil': # is bitmap font
				self.font = ImageFont.load(str(self.font))
			elif ext in '.ttf .otc .ttc': # is truetype font
				self.font = ImageFont.truetype(str(self.font), round(15 * self.font_scale))
			self.custom_font = True

	def get_size(self, char):
		if self.custom_font == False:
			self.size = cv2.getTextSize(text=char, fontFace=self.font, fontScale=self.font_scale, thickness=self.thickness)[:2][0]
		else:
			self.size = self.font.getsize(text=char, stroke_width=self.thickness)
		return self.size

	def get_avg_size(self, chars):
		w, h = self.get_all_sizes(chars)
		self.avg_size = (round(int(np.mean(w))), round(int(np.mean(h))))
		return self.avg_size

	def get_smallest_size(self, chars):
		w, h = self.get_all_sizes(chars)
		self.smallest_size = (round(int(min(w))), round(int(min(h))))
		return self.smallest_size

	def get_biggest_size(self, chars):
		w, h = self.get_all_sizes(chars)
		self.biggest_size = (round(int(max(w))), round(int(max(h))))
		return self.biggest_size

	def get_all_sizes(self, chars):
		"""
		get all font sizes int the character set
		"""
		chars = list(str(chars))
		widths = []
		heights = []
		for i in chars:
			if self.custom_font == False:
				w, h = cv2.getTextSize(text=str(i), fontFace=self.font, fontScale=self.font_scale, thickness=self.thickness)[:2][0]
			else:
				w, h = self.font.getsize(text=str(i), stroke_width=self.thickness)

			widths.append(w)
			heights.append(h)

		return widths, heights