#!/usr/bin/python
try:
	from os.path import expanduser 
	execfile(expanduser('~/public_html/main/templates/default.py'))
except:
	import sys, cgi
	exc_info = sys.exc_info()

	try:
		if not sys._finishedprintingheader: raise AttributeError
	except AttributeError: print 'Content-Type: text/html\n'

	try:
		import random
		randint = random.randint(10000,99999)
		print '''<style>#_python_error_%s h3, #_python_error_%s pre {font-family:courier,monospace; margin:0;} #_python_error_%s pre {white-space:pre-wrap !important; font-size:8pt;}</style>'''%(randint,randint,randint)
	
		print '''<title>Error</title><div id="_python_error_%s" style="color:#a10; background-color:#ffe; border:1px solid #a10; padding:2px; float:none; max-width: 600px; text-align:left; font-size:10pt; font-family:verdana,arial,serif;">'''%(randint)
	
		print '''<div onclick="document.getElementById('_python_error_details_%s').style.display='block'">An internal server error (Python) occured.</div>'''%(randint)
		
		print '''<div id="_python_error_details_%s" style="display:none;">Details:'''%(randint)
	
		cgi.print_exception(exc_info[0],exc_info[1],exc_info[2])
	
		print '''</div></div>'''

	except:
		cgi.print_exception(exc_info[0],exc_info[1],exc_info[2])
		print '''<hr>'''
		exc_info = sys.exc_info()
		cgi.print_exception(exc_info[0],exc_info[1],exc_info[2])
