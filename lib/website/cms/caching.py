#!/usr/bin/env python

from website import io
import files

class Cacher:
	
	def __init__(self, path='.'):
		import os.path
		self.file = os.path.join(path, files.CACHE_FILE)

	def read(self):
		try: return io.read(self.file)
		except: self.raiseerror()		
		
	def write(self, content):
		try: io.write(self.file, content)
		except: self.raiseerror()

	def raiseerror(self):
		try:
			from website import errors
			errors.defaulterror.catch(silent=True)
			return ''
		except:
			import sys, traceback
			exc_info = sys.exc_info()
			from website.html import make_exc
			return make_exc('<br>\n'.join(traceback.format_exception(exc_info[0], exc_info[1], exc_info[2])))

cache = Cacher()