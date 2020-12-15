import sys
import random
import os

"""
 Progressbar module
"""

class Progress:
	"""
	Progressbar class 
	"""
	def __init__(self, total, item='process', status=''):
		self.count = 0
		self.total = total
		self.status = status
		self.item = item 
		self.bar_len = 50
		self.filled_len = None
		self.precents = None
		self.bar = None
		self.title = (self.status  + ' ' + self.item).upper()
		if sys.platform == 'win32' or sys.platform == 'win64':
			os.system('color')
		print('\33[32m', self.title, '\033[0m' )

	def build(self):
		"""
		Print the progressbar
			-Auto increment
		"""
		self.count +=1
		self.filled_len = int(round(self.bar_len * self.count / float(self.total)))
		self.percent = round(100.0 * self.count / float(self.total), 1)
		self.bar = '█' * self.filled_len + '-' * (self.bar_len - self.filled_len)
		loader = ['\\', '|', '/', '-'][random.randint(0, 3)]			
		sys.stdout.write(' Progress: %s %s %s[%s] %s%s %s %s -- %s -- \r' % (f'{self.count} / {self.total}', self.item, '\33[32m',self.bar, self.percent, '%', loader, '\033[0m', self.status))
		
		sys.stdout.flush()

	def new_status(self, status, total):
		"""
		Reset the progressbar adn add new status
		"""
		self.total = total
		self.status = status
		self.item = item
		self.count = 0
