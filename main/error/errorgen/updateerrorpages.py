def makeexc(error):
	import random
	randint = random.randint(10000,99999)
	html = ''
	
	html +=  '''<style>#_script_error_%s h3, #_script_error_%s pre {font-family:courier,monospace; margin:0;} #_script_error_%s pre {white-space:pre-wrap !important; font-size:8pt;}</style>'''%(randint,randint,randint)

	html +=  '''<title>Error</title><div id="_script_error_%s" style="color:#a10; background-color:#ffe; border:1px solid #a10; padding:2px; float:none; max-width: 600px; text-align:left; font-size:10pt; font-family:verdana,arial,serif; white-space:pre-wrap;">'''%(randint)
	
	html += '''<div onclick="document.getElementById('_script_error_details_%s').style.display='block'">An internal server error occured.</div>'''%(randint)
	
	html += '''<div id="_script_error_details_%s" style="display:none; font-family: courier, monospace;">Details:\n'''%(randint)

	html += error

	html += '''</div></div>'''
	
	return html

## IOBlock 1.0.1.1 ##
def decode(s):
	if type(s) == unicode: return s
	elif type(s) == str:
		try: return s.decode('utf-8')
		except UnicodeDecodeError: return progressivedecode(s)
	elif s == None: return
	else: raise TypeError('Must be string or Unicode.')
def progressivedecode(s):
	u = u''
	for c in s:
		try: u += c.decode('utf-8')
		except UnicodeDecodeError: u += u'?'
	return u
def encode(s):
	if type(s) == str: return s
	elif type(s) == unicode: return s.encode('utf-8')
	elif s == None: return
	else: raise TypeError('Must be string or Unicode.')
def read(filepath):
	fr = open(filepath, 'r')
	try: content = fr.read()
	except: fr.close();	raise
	decodedcontent = decode(content)
	fr.close()
	return content
def write(filepath, content):
	fw = open(filepath, 'w')
	encodedcontent = encode(content)
	try: fw.write(encodedcontent)
	except: fw.close(); raise
	fw.close()
def append(filepath, content):
	fa = open(filepath, 'a')
	encodedcontent = encode(content)
	fa.write(encodedcontent)
	fa.close()
def touch(filepath): return append(filepath, '')
## / IOBlock ##

def readscript(script):
	import subprocess
	shellout = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	shellout.wait()
	return shellout.stdout.read(), shellout.stderr.read()

def readpythonscript(pyscript):
	return readscript(['python', pyscript])

def fmtreadscript(script):
	c = readscript(script)
	html = ''
	html += c[0]
	if c[1]: html += makeexc(c[1])
	return html

def fmtreadpythonscript(pyscript):
	return fmtreadscript(['python', pyscript])



if __name__ == '__main__':
	import sys
	print "Content-Type: text/html\n"
	sys._finishedprintingheader = True


	import os, sys
	filelist = filter(lambda x: x[0].isdigit(), os.listdir('.'))
	filelist.sort()
	#return `filelist`
	
	execfile(os.path.expanduser('~/public_html/main/templates/applytemplate.py'))


	tpath = os.path.expanduser('~/public_html/main/templates/maintemplate.html')
	dpath = 'parts.html'
	content = read(tpath)
	
	for fn in filelist:
		ups = [os.path.expanduser('~/public_html/main/error/errorgen/'+fn)]
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
		
		write(os.path.expanduser('~/public_html/main/error/'+fn+'.shtml'), content)

print 'Done'
