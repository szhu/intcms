#!/usr/bin/python


import os
execfile(os.path.expanduser('~/public_html/main/templates/applytemplate.py'))
tpath = os.path.expanduser('~/public_html/main/templates/maintemplate.html')
dpath = 'parts.html'
content = read(tpath)

ups = [os.getcwd()]
i = 0
while i<100:
	i += 1
	if len(ups[-1]) <= len(os.path.expanduser('~/public_html/')): break
	ups += [os.path.split(ups[-1])[0]]
else: raise Exception
ups.reverse()

for up in ups:
	try: content = applyparts(os.path.join( up, 'parts-root.html'), content)
	except IOError: pass
content = applyparts(dpath, content)

print "Content-Type: text/html\n"
sys._finishedprintingheader = True

print content
