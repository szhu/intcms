#!/usr/bin/python

APP_NAME = 'interestinglythere'
from os.path import expanduser

def read_settings_file(filename):
	from os.path import join, expanduser
	f = open( expanduser(join('~/.intcms', APP_NAME, filename)) )
	try: contents = f.read().strip()
	finally: f.close()	
	return contents

import sys, os

os.WEB_ROOT = expanduser( read_settings_file('web_root.txt') )
os.WEB_LIB = expanduser( read_settings_file('web_lib.txt') )
sys.path.append(os.WEB_LIB)



def display():
	import os, sys

	from website import io, cms
	
	errorcodes = [401, 403, 404, 500, '500-cms']
	writepath = 'pages/%s.shtml'
	indexpath = 'pages/index.html'
	templatepath = 'templates/%s'
	displaypath = '%s\n'
	
	os.chdir('..')
	html = ''
	# html += '''<title>Updating pages...</title>\n'''
	html += '''<pre style="white-space: pre-wrap">\n'''
	try:
		for num in errorcodes:
			html += displaypath%num
			doc = cms.display(templatepath%num)
			io.write(writepath%num, doc)
		#io.write(indexpath, '')
		html += 'Done.'
	finally: 
		html += '''</pre>'''
	return html

print display()
