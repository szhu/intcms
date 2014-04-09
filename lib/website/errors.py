#!/usr/bin/env python

'''Writes Python server errors to error log file as HTML'''

import os

class ErrorOut:
	from website.cms.files import getfullpath

	default_html_log_path = getfullpath('$WEB_ROOT/system/logs/python/python.log.html')
	default_text_log_path = getfullpath('$WEB_ROOT/system/logs/python.log.txt')
	
	def __init__(self, htmlpath = None, textpath = None):
		if htmlpath == None: self.htmlpath = self.default_html_log_path
		else: self.htmlpath = htmlpath
		if htmlpath == None: self.textpath = self.default_text_log_path
		else: self.textpath = textpath

	def write(self, content):
		import sys
		try: self.catch(content)
		except:
			import cgi
			if not ("_finishedprintingheader" in dir(sys) and sys._finishedprintingheader): print 'Content-Type: text/html\n'
			exc_info = sys.exc_info()
			cgi.print_exception(exc_info[0],exc_info[1],exc_info[2])
	
	def lowlevelwrite(self, path, content):
		f = open(path, 'a')
		try: f.write(content)
		finally: f.close()

	def catch(self, content=None, channel=None, exc_info=None, silent=False):
		import sys
		if not exc_info: exc_info = sys.exc_info()
		
		plainhtml = False
		if exc_info == (None, None, None) and channel!='html':
			self.lowlevelwrite(self.textpath, content)
		
		else:
			import time, traceback
			from website import html
			
			fmtexc = traceback.format_exception(exc_info[0],exc_info[1],exc_info[2])
			msg = ''
			msg += '''<div class=error>\n'''
			msg += time.strftime('''<div class=datetime><span class=date>%A, %m/%d/%Y</span> <span class=time>%I:%M:%S %p (%Z)</span></div>''')

			if not fmtexc:
				msg += '''<div class=errormessage>An error occurred:<br>''' + html.quote(`exc_info`+'\n'+`fmtexc`) + '''</div>\n'''
			elif channel=='html':
				msg += '''<div class=errormessage>''' + html.quote(content) + '''</div>\n'''
			else:
				msg += '''<pre class=traceback>''' + html.quote(''.join(fmtexc[1:-1]).strip())  + '''</pre>\n'''
				msg += '''<div class=errormessage>''' + html.quote(fmtexc[-1].strip()) + '''</div>\n'''
			msg += '''</div>\n\n'''

			self.lowlevelwrite(self.htmlpath, msg)

		if not ("_finishedprintingheader" in dir(sys) and sys._finishedprintingheader) and not silent:
			sys._finishedprintingheader = True
			print 'Status: 500 Internal Server Error'
			print 'Content-Type: text/html\n'
			from website import io
			try:
				from website.cms.files import getfullpath
				errorcontent = io.read(getfullpath('$WEB_ROOT/main/error/pages/500-cms.shtml'))
			except IOError:
				io.append('~/logs/python.log.txt', "\nCustom error page wasn't found! :(\n\n")
				print '''<title>500 Internal Server Error</title>'''
				print '''<h1>500 Internal Server Error</h1>'''
				print '''<p>So the server had an error. But the good news is that the error was caught by this neat little wrapper code and was written a log file, which Sean Zhu will look at, because he doesn't want other people to have to deal with an error message like this.</p>'''
				print '''<p>Well, sorry about the error. Uh, you can...uh... <a href="http://breadfish.co.uk/">go here</a>?</p>'''
			else:
				try: errorcontent = errorcontent.replace('''<!--#echo var="REQUEST_URI" -->''', os.environ['REQUEST_URI'])
				except AttributeError: pass
				print errorcontent
			

	def enable(self):
		import sys
		sys.stderr = self

defaulterror = ErrorOut()

def log(content, returnvalue=None):
	from website import errors
	defaulterror.catch(content=str(__name__)+':\n'+str(content), channel='html', silent=True)
	return returnvalue