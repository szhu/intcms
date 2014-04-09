#!/usr/bin/env python

from os.path import expanduser

def read_settings_file(filename):
	from os.path import join, expanduser
	f = open( expanduser(join('~/.intcms', APP_NAME, filename)) )
	try: contents = f.read().strip()
	finally: f.close()
	return contents
	

try:
	import os, sys

	page_name = (os.getenv('REQUEST_URI') or '').lstrip('/')
	os.chdir('../../'+page_name)

	os.WEB_ROOT = expanduser( read_settings_file('web_root.txt') )
	os.WEB_LIB  = expanduser( read_settings_file('web_lib.txt') )

	sys.path.append(os.WEB_LIB)
	from website import cms, http
	content = cms.display()
	http.header.html(); http.header.close()
	print content
	# print os.environ

except:
	import sys, cgi
	exc_info = sys.exc_info()
	if not ("_finishedprintingheader" in dir(sys) and sys._finishedprintingheader): print 'Content-Type: text/html\n'; sys._finishedprintingheader=True;
	cgi.print_exception(exc_info[0],exc_info[1],exc_info[2])
