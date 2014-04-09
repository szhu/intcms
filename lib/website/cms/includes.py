#!/usr/bin/env python

import os
from website import io
from website.io.web import read as readurl
from files import getfullpath


def readscript(script):
	import subprocess
	shellout = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	shellout.wait()
	return shellout.stdout.read(), shellout.stderr.read()

def readpythonscript(pyscript):
	import os
	return readscript(['python', getfullpath(pyscript)])

def fmtreadscript(script):
	c = readscript(script)
	html = ''
	html += c[0]
	if c[1]: return silenterror('in fmtreadscript:\n'+c[1], '')
	return html

def fmtreadpythonscript(pyscript):
	return fmtreadscript(['python', getfullpath(pyscript)])

def include_python(sobj):
	obj = eval(sobj)
	if type(obj) != dict: raise TypeError('Passed object must be dict.')
	k = obj.keys()
	if 'import' in k: exec('import '+obj['import'])
	if 'execfile' in k: execfile(getfullpath(obj['execfile']))
	if 'exec' in k: exec(obj['execfile'])
	if 'eval' in k: return eval(obj['eval'])

def include_plaintext(x):
	from website import html 
	return html.quote(io.read(getfullpath(x)))

includes_list = {
	'include': lambda x: io.read(getfullpath(x)),
	'include-plaintext': include_plaintext,
	'curl': readurl,
	'execfile': fmtreadpythonscript,
	'python_shell': fmtreadpythonscript,
	'python': include_python,
}

def useinclude(id, content):
	try:
		if id in includes_list.keys(): return str(includes_list[id](content))
		else: return '<!--'+content+'-->'
	except:
		try:
			from website import errors
			errors.defaulterror.catch(silent=True)
			return ''
		except:
			import sys, traceback
			exc_info = sys.exc_info()
			from website.html import make_exc
			return make_exc('<br>\n'.join(traceback.format_exception(exc_info[0], exc_info[1], exc_info[2])))

def silenterror(content, toreturn):
	from website import errors
	errors.defaulterror.catch(content='website.cms.includes.py:\n'+content, channel='html', silent=True)
	return toreturn