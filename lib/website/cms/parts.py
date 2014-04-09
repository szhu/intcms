#!/usr/bin/env python

def applyparts(dpath, content):
	from website import io
	import utils, includes, re

	dcontent = io.read(dpath)
	dparts = re.split('\s*<!--###+-->\s*', dcontent)
	parts = {}
	for rawpart in dparts:
		rawpart = rawpart.strip()
		if not rawpart: continue
		header, part = splitfirstline(rawpart)
		m = re.match(r'\s*<!--%?(.+)%?-->\s*', header)
		if not m: continue
		id = m.group(1)
		parts[id] = re_replace(r'<!--([a-z/ _-]+)\s*:\s*(.+)\s*-->', lambda m:includes.useinclude(m.group(1),m.group(2)), part)

	def getpart(oldstring, id):
		try: return parts[id]
		except KeyError: return oldstring
	content = re_replace(r'(<!--)?%([a-z/ _-]+)%(-->)?', lambda m:getpart(m.group(0),m.group(2)), content)
	return content

def splitfirstline(s):
	import re
	r = re.split('[\n\r]+', s, 1)
	if len(r) == 1: r += ['']
	return r

def re_replace(pattern, repl, old):
	import re
	writehead = 0; new = ''
	matches = re.finditer(pattern, old)
	for m in matches:
		new += old[writehead:m.start(0)]
		new += repl(m)
		writehead = m.end(0)
	new += old[writehead:]
	return new

from website.errors import log
# def silenterror(content, toreturn=None):
# 	from website import errors
# 	errors.defaulterror.catch(content='website.cms.parts.py:\n'+content, channel='html', silent=True)
# 	return toreturn