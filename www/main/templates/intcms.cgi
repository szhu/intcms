#!/usr/bin/python

try:
	APP_NAME = 'interestinglythere'
	from os.path import expanduser

	def read_settings_file(filename):
		from os.path import join, expanduser
		f = open( expanduser(join('~/.intcms', APP_NAME, filename)) )
		try: contents = f.read().strip()
		finally: f.close()	
		return contents


	execfile(expanduser( read_settings_file('web_script.txt') ))

except:
	import sys, cgi
	exc_info = sys.exc_info()
	if not ("_finishedprintingheader" in dir(sys) and sys._finishedprintingheader): print 'Content-Type: text/html\n'; sys._finishedprintingheader=True;
	cgi.print_exception(exc_info[0],exc_info[1],exc_info[2])
