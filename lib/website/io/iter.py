#!/usr/bin/env python

import os.path

def readlines(filepath):
	fr = open(os.path.expanduser(filepath), 'r')
	try:
		for line in fr.readlines(): yield line.strip()
		fr.close()
	except: fr.close(); raise

def readwords(filepath):
	for line in self.readlines(os.path.expanduser(filepath)): yield line.split()
