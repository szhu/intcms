#!/usr/bin/env python

def read(url):
	import urllib
	filehandle = urllib.urlopen(url)
	content = filehandle.readlines()
	filehandle.close()
	return ''.join(content)
