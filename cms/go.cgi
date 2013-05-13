#!/usr/bin/env python

ERROR_TEMPLATE_START = '''<style>
#_python_error_%s, #_python_error_%s * {
	margin: 0;
	padding: 0;
	border: 0;
	font-size: 100%;
	font: inherit;
	vertical-align: baseline;
}

#_python_error_%s {
	background-color: #ffe;
	border: 1px solid #a10;
	color: #a10;
	float: none;
	font-family: 'Lucida Grande', Tahoma, Arial, serif;
	font-size: 15px;
	max-width: 600px;
	margin: 5px auto;
	padding: 8px;
	text-align: left;
}

#_python_error_%s h3 {
	font-family: Menlo, 'Courier New', monospace;
	font-weight: bold;
	font-size: 12px;
}

#_python_error_%s pre {
	font-family: Menlo, 'Courier New', monospace;
	font-size: 12px;
	white-space: pre-wrap !important;
}

#_python_error_details_%s, ._python_error_details_%s {
	border-top: 1px solid #a10;
	margin-top: 0.7em;
	padding-top: 0.7em;
}
</style>
<title>Error</title>
<div id="_python_error_%s">
<div onclick="document.getElementById('_python_error_details_%s').style.display=''">An internal server error occured.</div>
<div id="_python_error_details_%s" class="_python_error_details_%s" style="display: none;">
'''
ERROR_TEMPLATE_END = '''
</div>
</div>'''

try:
	try:
		import os
		if os.environ['QUERY_STRING'] == 'cprofile': import cProfile; cProfile.run("execfile('main.py')", 'cProfile.out')
		else: raise KeyError
	except KeyError:
		execfile('main.py')

except:
	import sys, cgi
	exc_info = sys.exc_info()

	try:
		if not sys._finishedprintingheader: raise AttributeError
	except AttributeError: print 'Status: 500 Internal Server Error\nContent-Type: text/html\n'

	try:
		import random
		rand = str(random.randint(10000,99999))
		print ERROR_TEMPLATE_START.replace('%s', rand)
		cgi.print_exception(exc_info[0],exc_info[1],exc_info[2])
		print ERROR_TEMPLATE_END.replace('%s', rand)

	except:
		print '''<h3>An internal server error occurred:</h3>'''
		cgi.print_exception(exc_info[0],exc_info[1],exc_info[2])
		print '''<hr>'''
		print '''<h3>In addition, another internal server error occurred while generating the error output:</h3>'''
		exc_info = sys.exc_info()
		cgi.print_exception(exc_info[0],exc_info[1],exc_info[2])