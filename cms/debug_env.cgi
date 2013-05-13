#!/usr/bin/env python

import sys, os
exc_info = sys.exc_info()
print 'Content-Type: text/plain\n'
print 'sys.argv:'
for arg in sys.argv:
	print ' ', repr(arg)
print

print 'os.environ:'
keys = os.environ.keys()
keys.sort()
for key in keys:
	print ' ', key, '=', repr(os.environ[key])