def listdir(path='.'):
	import os
	from website.cms.files import all_special_files as cmsfiles, TOP_FILE
	items = os.listdir(path)
	
	mainlist = []
	others = []
	specialfiles = ['.DS_Store', '.htaccess', 'index.cgi', 'htcms.cgi'] + cmsfiles
	for i in xrange(len(items)):
		x = items[i]
		if ( x.replace('~', '') in specialfiles or x.startswith('htscript') or x.startswith('._') ):
			others += [x]
		else: mainlist += [x]
	
	mainlist.sort(); others.sort()

	s = ''
	s += '''<div id="dirlist">'''
	if not os.path.exists(TOP_FILE): s += '''<div><a href="..">Parent Directory</a></div>'''
	s += '''<ul>'''
	for item in mainlist:
		if os.path.isdir(item): item += '/'
		s +=  '''<li><a href="%s">%s</a></li>'''%(item,item)
	s +=  '''</ul>'''
	if others: s +=  '''<div>Others: %s'''%(', '.join(others)) + '''</div>'''
	s += '''</div>'''
	
	return s