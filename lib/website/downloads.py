#!/usr/bin/env python

'''Download files'''

import os
from website import io

def download(f):
	f = os.path.expanduser(f)

	if os.path.exists(f):
		content = io.read(f)
		print "Content-Type: application/octet-stream"
		print 'Content-disposition: attachment; filename="%s"'%os.path.split(f)[1]
		print
		print content

	else: raise OSError("File %s doesn't exist."%f)