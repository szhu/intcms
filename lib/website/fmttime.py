#!/usr/bin/env python

def currentyear():
	import time
	return time.struct_time(time.localtime())[0]