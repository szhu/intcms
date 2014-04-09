#!/usr/bin/env python


def mkdate(dt=None):
	'''Return a string representation of a date according to RFC 1123
	(HTTP/1.1). The supplied date must be in UTC.
	http://stackoverflow.com/questions/225086'''
	if dt==None: import time; dt = time.gmtime()
	weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.tm_wday]
	month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
			 "Oct", "Nov", "Dec"][dt.tm_mon - 1]
	return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.tm_mday, month,
		dt.tm_year, dt.tm_hour, dt.tm_min, dt.tm_sec)


def download(f, displayedfilename=None):
	import os
	from website import io
	f = os.path.expanduser(f)
	if os.path.exists(f):
		content = io.read(f)
		if not displayedfilename: displayedfilename = os.path.split(f)[1]
		header.download(displayedfilename)
		print content
	else: raise OSError("File %s doesn't exist."%f)



class Header:

	def __init__(self): self.isfinished = False
	def hardcheck(self):
		if self.finished(): raise HTTPHeaderAlreadyPrintedError('HTTP header has already finished.')
	def finished(self):
		import sys
		return self.isfinished or ("_finishedprintingheader" in dir(sys) and sys._finishedprintingheader)
	def close(self):
		import sys
		print
		self.isfinished = True; sys._finishedprintingheader = True

	def download(self, displayedfilename):
		self.hardcheck()
		print "Content-Type: application/octet-stream"
		print 'Content-disposition: attachment; filename="%s"'%displayedfilename
		self.close()

	def html(self):
		if not self.finished(): print 'Content-Type: text/html'; return True
		else: return False

	
class HTTPError(Exception):
	def __init__(self, value=''):
		self.value = value
	def __str__(self):
		return self.value

class HTTPHeaderAlreadyPrintedError(HTTPError):
	def __init__(self, value=''):
		self.value = value
	def __str__(self):
		return self.value

		
header = Header()