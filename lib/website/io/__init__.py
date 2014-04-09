#!/usr/bin/env python

import os.path, iter, web
defaultenc='utf-8'

def decode(s, enc=defaultenc):
	if not enc: return s
	if type(s) == unicode: return s
	elif type(s) == str:
		try: return s.decode(enc)
		except UnicodeDecodeError: return progressivedecode(s,enc)
	elif s == None: return
	else: raise TypeError('Must be string or Unicode.')
def progressivedecode(s, enc):
	if not enc: return s
	u = u''
	for c in s:
		try: u += c.decode(enc)
		except UnicodeDecodeError: u += u'?'
	return u
def encode(s, enc=defaultenc):
	if not enc: return s
	if type(s) == str: return s
	elif type(s) == unicode: return s.encode(enc)
	elif s == None: return
	else: raise TypeError('Must be string or Unicode.')


def read(filepath):
	fr = open(os.path.expanduser(filepath), 'r')
	try: content = fr.read()
	finally: fr.close()
	return content
def readlines(filepath):
	return [line for line in iter.readlines(filepath)]
def readwords(filepath):
	return [line.split() for line in readlines(filepath)]
	
def write(filepath, content):
	fw = open(os.path.expanduser(filepath), 'w')
	try: fw.write(content)
	finally: fw.close()
def append(filepath, content):
	fa = open(os.path.expanduser(filepath), 'a')
	try: fa.write(content)
	finally: fa.close()
def touch(filepath):
	return append(filepath, '')
