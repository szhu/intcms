#!/usr/bin/env python

import os


#MAIN_TEMPLATE_PATH = os.path.join(WEB_ROOT, 'main/templates/main.html')
PARTS_FILE =       'htpartsf.html'
PARTS_ROOT =       'htpartsd.html'
PARTS_BOTH =       'htpartsa.html'
TOP_FILE =         '.htroot'
METADATA_FILE =    'htmetadata.txt'
CACHE_FILE =       'htcachedindex.html'
CACHE_BACKUP_FILE ='htcachedindex.bak.html'
RECURSION_LIMIT = 1000

def getfullpath(path):
	import os.path
	return os.path.expanduser(path.replace('$WEB_ROOT',os.WEB_ROOT).replace('$WEB_LIB',os.WEB_LIB))


all_special_files = [PARTS_FILE, PARTS_ROOT, PARTS_BOTH, TOP_FILE, METADATA_FILE, CACHE_FILE, CACHE_BACKUP_FILE]

PATHDEBUG = False
LOGFILE = '~/logs/python.log.txt'

def isupdated(path, cachetime):
	mtime = getmtime(path)
	if cachetime < mtime: return True
	else: return False

def getmtime(path): import os; return os.stat(path).st_mtime
def getage(t): import time; return time.time() - t
#def datetooold

def appendifexists(l, cd, file):
	import os.path
	path = os.path.join(cd, file)
	if PATHDEBUG:
		from website import io; io.append(LOGFILE, `path`)
	if os.path.exists(path):
		l.append(path)
		if PATHDEBUG: io.append(LOGFILE, ' *\n')
		return True
	else:
		if PATHDEBUG: io.append(LOGFILE, '\n')
		return False

def getpaths(dirpath=None, maxage=None):
	import os;  from os.path import expanduser
	cd = os.getcwd()
	if dirpath: cd = os.path.join(cd, expanduser(dirpath))

	if PATHDEBUG: from website import io; io.append(LOGFILE, '\n\n%s :\n'%cd)
	
	paths = []
	class notupdated: pass

	for i in xrange(RECURSION_LIMIT):
		for (old, new) in [('parts.html', 'htpartsf.html'), ('parts-root.html', 'htpartsa.html')]:
			c_old = os.path.join(cd, old); c_new = os.path.join(cd, new)
			if os.path.exists(c_old) and not os.path.exists(c_new):
				os.rename(c_old, c_new)
				from website import io; io.append(LOGFILE, '%s -> %s\n'%(c_old, c_new))

		if i != 0: appendifexists(paths, cd, PARTS_ROOT)
		elif not appendifexists(paths, cd, PARTS_FILE): paths.append(getfullpath('$WEB_ROOT/main/templates/listdir.html'))
		appendifexists(paths, cd, PARTS_BOTH)
		topfilepath = os.path.join(cd, TOP_FILE)
		if os.path.exists(topfilepath):
			from website import io
			MAIN_TEMPLATE_PATH = getfullpath(io.read(topfilepath).strip())
			break
		cd = os.path.split(cd)[0]
	paths.append(expanduser(MAIN_TEMPLATE_PATH))
	
	CACHE_FILE_cd = os.path.join(cd, CACHE_FILE)
	if os.path.exists(CACHE_FILE_cd): cachetime = getmtime(CACHE_FILE_cd)
	else: cachetime = 0

	for path in paths:
		if isupdated(path, cachetime):
			paths.reverse(); return (True, paths)
	else:
		paths = (False, CACHE_FILE_cd)

	
