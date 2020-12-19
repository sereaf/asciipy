import math
import cv2
import os
import sys
import time
from .image import AsciiImage
from .progress import Progress
from .editor.utils import *

class AsciiVideo:
	""" 
		Class for the video to asciify and call the output action
	"""
	def __init__(self, pathIn):
		self.pathIn = pathIn
		self.size = None
		self.fps = None
		self.video_length = None
		self.total_frames = 0
		self.video = cv2.VideoCapture(str(self.pathIn))
		self.size = (math.ceil(int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))), math.ceil(int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
		self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
		self.video_length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
		self.name = os.path.basename(self.pathIn)

	def get(self):
		return self.video
	
	def stop(self):
		self.video.release()

	def cap(self):
		return cv2.VideoCapture(str(self.pathIn))

	@timeit
	def ascii_video(self, output='', audio=False, option='colored', font=2, save_as='', scale='fit', density_flip=False, character_space='', chars=None, font_scale=1):
		"Create and save ascii video"
		video = self.cap()
		output = get_path_out(self.pathIn, output)
		b_name = os.path.basename(self.pathIn)
		p = Progress(self.video_length, 'frames', 'Processing')
		if save_as is None or save_as == '':
			save_as = 'mp4v'
		fourcc = cv2.VideoWriter_fourcc(*str(save_as))
		if audio:
			import tempfile
			temp_dir = tempfile.gettempdir()
			new_video = os.path.join(temp_dir, 'asciipy_video')+os.path.splitext(self.pathIn)[1]
		else:
			new_video = output+os.path.splitext(self.pathIn)[1]
		videoOut = cv2.VideoWriter(new_video, fourcc, self.fps, self.size)
		total_frames = 0
		while total_frames < self.video_length: #video.isOpened()
			ret, frame = video.read()
			total_frames += 1
			p.build()
			i = AsciiImage(frame)
			img = i.ascii_img(action='return', option=option, font=font, scale=scale, density_flip=density_flip, character_space=character_space, chars=chars, font_scale=font_scale)
			videoOut.write(img)
		self.stop()
		videoOut.release()
		if audio:
			import ffmpeg
			temp_file_audio = os.path.join(temp_dir, "asciipy_audio.wav")
			input_video = ffmpeg.input(self.pathIn)

			final = output+os.path.splitext(self.pathIn)[1]

			stream = (
				ffmpeg
				.input(self.pathIn)
				.output(temp_file_audio)
				.overwrite_output()
				.run()
			)

			audio_file = ffmpeg.input(temp_file_audio)
			new_v = ffmpeg.input(new_video)
			ffmpeg.concat(new_v, audio_file, v=1, a=1).output(final).overwrite_output().run()

			os.remove(new_video)
			os.remove(temp_file_audio)

	@timeit
	def ascii_terminal(self, option='colored', action='return', scale='fit', density_flip=False, chars=None, character_space='', clear=False, terminal_spacing=None, ratio_to='width'):
		"Create and print ascii video to the terminal"
		video = self.cap()
		total_frames = 0
		char_arr = []
		if action == 'return':
			p = Progress(self.video_length, 'frames', 'Processing')
		while total_frames < self.video_length:
			ret, frame = video.read()
			total_frames += 1
			i = AsciiImage(frame)
			if total_frames < self.video_length:
				clear = True
			else:
				clear = False
			if action == 'return':
				p.build()
				ch, t_w, t_h = i.ascii_terminal(option=option, action=action, scale=scale, density_flip=density_flip, character_space=character_space, chars=chars, clear=clear, ratio_to=ratio_to)
				char_arr.append(ch)
			elif action == 'save' or action == 'play':
				i.ascii_terminal(option=option, action=action, scale=scale, density_flip=density_flip, character_space=character_space, chars=chars, clear=clear, terminal_spacing=terminal_spacing, ratio_to=ratio_to)
		if action == 'return':
			t1 = cv2.getTickCount()
			for i in range(len(char_arr)):
				e1 = cv2.getTickCount()
			
				if i < len(char_arr)-1:
					clear = True
				else:
					clear = False
				print_terminal(char_arr[i], (t_w, t_h), terminal_spacing, clear)
				e2 = cv2.getTickCount()
				exec_time = (e2 - e1)/cv2.getTickFrequency()
				# if print time is less than 1/fps --> than sleep till it equals 1/fps
				if exec_time < (1/self.fps):
					time.sleep((1/self.fps)-exec_time)
				else:
					pass
			# print full print data
			t2 = cv2.getTickCount()
			render_time = (t2 - t1)/cv2.getTickFrequency()
			print('\n')
			print(f'{self.name} at {self.video_length // render_time} fps - print time {round(render_time)} seconds (original - fps {self.fps} - length {self.video_length // self.fps} seconds)')
		self.stop()

	@timeit
	def ascii_txt(self, output=None, option='bandw', action='save', scale='fit', density_flip=False, chars=None, character_space='', clear=False):
		"""Save ascii video by frames into a .txt file"""
		video = self.cap()
		total_frames = 0
		char_arr = []
		output = get_path_out(self.pathIn, output)
		while total_frames < self.video_length:
			ret, frame = video.read()
			total_frames += 1
			i = AsciiImage(frame)
			i.ascii_txt(output=output, option=option, action=action, scale=scale, density_flip=density_flip, character_space=character_space, chars=chars, clear=clear)
		self.stop()

