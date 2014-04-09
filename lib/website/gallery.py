template = '''<a class="galitem">
  <span class="galcaption">%s</span>
  <img src="%s" /></a>
'''

def display(datafile='htgallery.txt'):
	import os
	from website import io

	imglist = io.read(datafile).strip().splitlines()
	

	s = ''
	s += '''<div class="htgallery">'''
	s += ''''''
	for item in imglist:
		parts = item.split('\t',1)
		url = parts[0]
		if len(parts) == 2: caption = parts[1]
		else: caption = ''
		s +=  template % (caption, url)
	s +=  ''''''
	s += '''</div>'''
	
	return s

def getcss():
	from website import io
	from cms import files

	return io.read(files.getfullpath('$WEB_ROOT/main/templates/gallery.css'))