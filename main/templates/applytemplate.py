#!/usr/bin/python

import sys

def lstripseqonce(s, seq):
	if s.startswith(seq): return s[len(seq):]
	else: return s
def rstripseqonce(s, seq):
	if s.endswith(seq): return s[:-len(seq)]
	else: return s

def decode(s):
	if type(s) == unicode: return s
	elif type(s) == str: return s.decode('utf-8')
	elif s == None: return
	else: raise TypeError

def encode(s):
	if type(s) == str: return s
	elif type(s) == unicode: return s.encode('utf-8')
	elif s == None: return
	else: raise TypeError

def replace_multiple(s, rdict, keyf=None, valf=None):
	identity = lambda x: x
	if keyf==None: keyf = identity
	if valf==None: valf = identity
	format = type(rdict)
	if format == dict:
		for key in rdict.keys(): s = s.replace(keyf(key), valf(rdict[key]))
	elif format in (tuple, list):
		for (key, val) in rdict: s = s.replace(keyf(key), valf(val))
	else: raise TypeError('dict, tuple, or list only')
	return s

def html_unicode_escape(s):
	new_s = ''
	for char in s:
		o = ord(char)
		if o > 127: new_s += '&#%s;' % str(o).zfill(4)
		else: new_s += char
	return new_s

def html_escape(s): 
	html_escapes = [('&', '&amp;'), ('"', '&quot;'), ('<', '&lt;'), ('>', '&gt;'), ('\n','<br>\n')]
	return replace_multiple(s, html_escapes)

def quotehtml(s): return html_unicode_escape(html_escape(s))


def write(filepath, contents):
	fw = open(filepath, 'w')
	try: fw.write(encode(contents))
	except: 
		fw.close()
		raise
	fw.close()

def read(filepath):
	fr = open(filepath, 'r')
	try: content = decode(fr.read())
	except: 
		fr.close()
		raise
	fr.close()
	return content


def readscript(script):
	import subprocess
	shellout = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	shellout.wait()
	return shellout.stdout.read(), shellout.stderr.read()

def readpythonscript(pyscript):
	return readscript(['python', pyscript])

def fmtreadscript(script):
	c = readscript(script)
	html = ''
	html += c[0]
	if c[1]: html += makeexc(c[1])
	return html

def fmtreadpythonscript(pyscript):
	return fmtreadscript(['python', pyscript])


def makeexc(error):
	import random
	randint = random.randint(10000,99999)
	html = ''
	
	html +=  '''<style>#_script_error_%s h3, #_script_error_%s pre {font-family:courier,monospace; margin:0;} #_script_error_%s pre {white-space:pre-wrap !important; font-size:8pt;}</style>'''%(randint,randint,randint)

	html +=  '''<title>Error</title><div id="_script_error_%s" style="color:#a10; background-color:#ffe; border:1px solid #a10; padding:2px; float:none; max-width: 600px; text-align:left; font-size:10pt; font-family:verdana,arial,serif; white-space:pre-wrap;">'''%(randint)
	
	html += '''<div onclick="document.getElementById('_script_error_details_%s').style.display='block'">An internal server error occured.</div>'''%(randint)
	
	html += '''<div id="_script_error_details_%s" style="display:none; font-family: courier, monospace;">Details:\n'''%(randint)

	html += error

	html += '''</div></div>'''
	
	return html

def useinclude(line):
	def readurl(url):
		import urllib
		filehandle = urllib.urlopen(url)
		content = filehandle.readlines()
		filehandle.close()
		return '\n'.join(content)
	def stripprompt(prompt):
		return lstripseqonce(line_s, prompt).strip()

	try:
		line_s = rstripseqonce(lstripseqonce(line.strip(), '<!--'), '-->').strip('%')
		if line_s.startswith('include:'): return read(os.path.expanduser(stripprompt('include:')))
		elif line_s.startswith('curl:'): return readurl(stripprompt('curl:'))
		elif line_s.startswith('execfile:'):  return fmtreadpythonscript(stripprompt('execfile:'))
		#execfile(os.path.expanduser(stripprompt('execfile:')), globals(), locals()); return locals()['include_text']()
		else: return line
	except:
		import sys, traceback
		html = ''
		exc_info = sys.exc_info()
	
		return makeexc('<br>\n'.join(traceback.format_exception(exc_info[0], exc_info[1], exc_info[2])))

def applyparts(dpath, content):

	dcontent = read(dpath)
	
	dparts = dcontent.split('<!--###')
	parts = []
	for dpart in dparts:
		dpart = dpart.strip()
		if dpart:
			rawpart = lstripseqonce(dpart.lstrip('#'), '-->').strip()
			lines = rawpart.splitlines()
			id = rstripseqonce(lstripseqonce(lines[0], '<!--'), '-->').strip('%')
			lines_included = map(useinclude, lines)
			part = '\n'.join(lines_included[1:]).strip()
			parts += [('<!--%'+id+'%-->', '<!--%'+id+'-toreplace%-->')]
			parts += [('%'+id+'%', part)]
			parts += [('<!--%'+id+'-toreplace%-->', part)]
	
	content = replace_multiple(content, parts, valf=html_unicode_escape)
	#print html_escape(content)
	return content