import argparse
from image import AsciiImage
from video import AsciiVideo
from editor.utils import *
import sys

""" Cli interface module """

prog = 'asciipy'
desc = 'This package lets you turn images and videos to ascii art and print it to terminal or save it in a supported format on your computer.'
epilog = 'Have fun asciifying!'

class Parser:
	def __init__(self, prog, desc, epilog):
		self.prog = prog
		self.desc = desc
		self.epilog = epilog
		self.parser = argparse.ArgumentParser(prog=self.prog, description=self.desc, epilog=self.epilog)

	def get(self):
		return self.parser

	def get_args(self):
		return self.parser.parse_args()

def main():
	p = Parser(prog, desc, epilog)
	parser = p.get()
	parser.add_argument('-f', '--file', type=str.lower, help='DEFAULT:-  DESC: Input file path (png, jpg, mp4)', action='store', required=True)
	parser.add_argument('-ac', '--action', type=str.lower, help='DEFAULT:\'save\' DESC: terminal / save / return / into txt file - output', default='save', action='store')
	parser.add_argument('-o', '--output', type=str.lower, help='DEFAULT:\'\'(input path or if that is not valid than first drive found) DESC: Output file path', default='', action='store')
	parser.add_argument('-oa', '--output-as', type=str.lower, choices=['save', 'terminal', 'txt'], help='DEFAULT: save DESC: output to terminal / txt file / or save as img / video', default='save', action='store')
	parser.add_argument('-op', '--option', type=str.lower, choices=['colored', 'bandw', 'filled', 'filled-bandw', 'full-filled', 'full-filled-bandw', '2char', '2char-bandw'], help='DEFAULT:\'colored\' DESC: Process options (colorfull / black and white / filled / 2char / 2char-b&w) - 2char one dark and one light char', default='colored', action='store')
	parser.add_argument('-ch', '--chars', type=str, help='DEFAULT:varies - depends on option DESC: List of characters to use in asciify process - from most dense to least (works with: colored, b&w, 2char, 2char-b&w)', default=None)
	parser.add_argument('-au', '--audio', help='DEFAULT:False DESC: With audio', action='store_true', default=False)
	parser.add_argument('-fo', '--font', type=str.lower,help='DEFAULT:\'2\'(cv2 font)  DESC: The font - integer for cv2 fonts or path for custom', default='2', action='store')
	parser.add_argument('-as', '--save-as', type=str.lower, help='DEFAULT:\'\'(input extension) DESC: Format of the output image or video (png / jpg or mp4 / avi)',  action='store')
	parser.add_argument('-s', '--scale', type=str.lower, help='DEFAULT:\'fit\' DESC: How many of the pixels should be turned to ascii (ex:. -s=0.55 = 55 precent of the pixels will be asciifyed)', default='fit')
	parser.add_argument('-df', '--density-flip', type=bool, help='DEFAULT:False DESC: If set to True the ascii characters chosen at dark pixels will be the least dense ones and at light pixels the denser characters.', default=False, action='store')
	parser.add_argument('-cs', '--character-space', type=str.lower, help='DEFAULT:\'\'(# - size) DESC: In font files some characters have different size. Get avg - average ; sm - smallest ; bg - biggest from fonts and use that spacing when putting it onto an image.', default='', action='store') # choices=['avg', 'sm', 'bg']
	parser.add_argument('-fs', '--font-scale', type=float, help='DEFAULT:\'1\'(default font size) DESC: Scale the font compared to the original size of it', default=1, action='store')
	parser.add_argument('-ts', '--terminal-size', nargs='+', type=int, help='DEFAULT:current terminal size or (53, 30)  DESC: ', default=None, action='store')
	parser.add_argument('-rt', '--ratio-to', type=str.lower, choices=['pass', 'width', 'height'], help='DEFAULT: width DESC: auto scale the width to the height of the input image in terminal or vice versa or pass - (no auto scaling)', default='width', action='store')
	parser.add_argument('-tspc', '--terminal-spacing', type=str, help='DEFAULT: None - () DESC: character dividing the characters printed to the terminal', default=None, action='store')
	parser.add_argument('-clr', '--clear', type=bool, help='DEFAULT: False - () DESC: clear the terminal after image printed', default=False, action='store')
	""" -h or --help for help """

	a = p.get_args()

	file_type = image_or_video(a.file)

	output_as = a.output_as

	if file_type == 'video':
		v = AsciiVideo(a.file)
		if output_as == 'save':
			v.ascii_video(output=a.output, option=a.option, font=a.font, save_as=a.save_as, scale=a.scale, density_flip=a.density_flip, character_space=a.character_space, chars=a.chars, font_scale=a.font_scale)
		elif output_as == 'terminal':
			v.ascii_terminal(option=a.option, action=a.action, scale=a.scale, density_flip=a.density_flip, character_space=a.character_space, chars=a.chars, ratio_to=a.ratio_to)
		elif output_as == 'txt':
			v.ascii_txt(output=a.output, option=a.option, action=a.action, scale=a.scale, density_flip=a.density_flip, chars=a.chars, clear=a.clear, character_space=a.character_space)
	elif file_type == 'image':
		i = AsciiImage(a.file)
		if output_as == 'save':
			i.ascii_img(action=a.action, output=a.output, option=a.option, font=a.font, save_as=a.save_as, scale=a.scale, density_flip=a.density_flip, character_space=a.character_space, chars=a.chars, font_scale=a.font_scale)
		elif output_as == 'terminal':
			i.ascii_terminal(option=a.option, action=a.action, scale=a.scale, terminal_size=a.terminal_size, density_flip=a.density_flip, chars=a.chars, ratio_to=a.ratio_to, terminal_spacing=a.terminal_spacing, clear=a.clear)
		elif output_as == 'txt':
			i.ascii_txt(output=a.output, option=a.option, action=a.action, scale=a.scale, density_flip=a.density_flip, chars=a.chars, clear=a.clear, character_space=a.character_space)

if __name__ == '__main__':
	main()

