import os
import sys
import cv2

"""
	Functions not related to image or video processing, but needed in the process of creating them
"""



def get_path_out(path_in, path_out):
	"""
	Get the right path for the output file
	"""
	if path_out is None or path_out == '':  #or os.path.exists(str(path_out)):
		if os.path.exists(str(path_in)):
			#output = os.path.join(os.path.dirname(path_in), os.path.splitext(os.path.basename(path_in))[0])
			output = os.path.splitext(path_in)[0] + '_ascii'
		else:
			output = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ][0]
	else:
		return path_out
	return output

def timeit(func):
	"""
	Timer decorator
	"""
	def timed(*args, **kw):
		if 'action' in kw and kw['action'] == 'return':
			if kw['action'] == 'return':
				result = func(*args, **kw)
		else:
			e1 = cv2.getTickCount()
			result = func(*args, **kw)
			e2 = cv2.getTickCount()
			t = (e2 - e1)/cv2.getTickFrequency()
			print('\n')
			print(f'Time spent in | seconds: {t} | ~~~ | minutes: {t/60} |')
		return result
	return timed

def print_terminal(char_arr, terminal_size, terminal_spacing='', clear=False):
	if terminal_spacing is None:
			terminal_spacing = ''
	terminal_width, terminal_height = terminal_size
	# loop by width, get that chunk of the list, join it and print it
	# the first join is for horizontaly between the chars and the second one vertically
	# the image will keep the same ratio if the horizontal join is a white space since there will be always one space vertically
	# could get the same ratio if double the chars - visually better than spaces
	for i in range(len(char_arr) // terminal_width):
			print((str(terminal_spacing).join(char_arr[terminal_width*(i-1):terminal_width*(i)])))
	
	if clear:
		print("\033[F"*(terminal_height), end='')
		print('\x1b[2K'*(terminal_height), end='')

image_extensions = ['.bmp', '.dib', '.pbm', '.pgm', '.ppm', '.pxm', '.pnm', '.sr', '.ras', '.hdr', '.pic', '.jp2', '.jpg', '.jpeg', '.webp', '.tiff', '.tif ', '.exr', '.png'] 
video_extensions = ['.mp4', '.avi', '.mov', '.mpeg', '.mpg', '.flv', '.wmv']

def image_or_video(file_path):
	""" Check if file extension is in supported video or image formats """
	file_type = None
	file_extension =  os.path.splitext(os.path.basename(file_path))[1]
	if file_extension in image_extensions:
		file_type = 'image'
	elif file_extension in video_extensions:
		file_type = 'video'
	else:
		raise  ValueError(f'Given file extension {file_extension} is not supported')

	return file_type