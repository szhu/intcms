#!/usr/bin/env python

def replace_multiple(s, replace_pairs):
	for (key, val) in replace_pairs: s = s.replace(key, val)
	return s

html_quote_replace_pairs = [
	('&',  '&amp;'),
	('"',  '&quot;'),
	('<',  '&lt;'),
	('>',  '&gt;'),
	('\n','<br>\n')
]
textarea_quote_replace_pairs = [
	('&',  '&amp;'),
	('<',  '&lt;'),
	('>',  '&gt;'),
]

def quote(s):
	return replace_multiple(s, html_quote_replace_pairs)

def textareaquote(s):
	return replace_multiple(s, textarea_quote_replace_pairs)

def unicode_escape(s):
	new_s = ''
	for char in s:
		o = ord(char)
		if o > 127: new_s += '&#%s;' % str(o).zfill(4)
		else: new_s += char
	return new_s

def make_exc(error):
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
