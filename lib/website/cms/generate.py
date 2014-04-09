#!/usr/bin/env python

import files, parts, re, caching
from website import io

def display(dirpath=None):
	isupdated, paths = files.getpaths(dirpath)
	if isupdated or True:
		content = io.read(paths[0])
		for i in xrange(1, len(paths)): content = parts.applyparts(paths[i], content)
		content = re.sub(r'\n?<!--%[\w-]+%-->\n?','',content)
# 		caching.cache.write ####
		return io.encode(content)
	else:
		return caching.cache.read()
