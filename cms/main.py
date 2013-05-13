#!/usr/bin/env python

import sys
import os

def print_page():
	context = current_page

	page_files = 'page.html', 'redirect-permanent.txt', 'redirect-temporary.txt', ''
	for i in range(len(page_files)):
		if current_page.exists_file(page_files[i]): break
	else:  # 404
		header = 'Status: 404 Not Found\nContent-Type: text/html'
		content = Resource('error', '404').read_file('page.html')['content']
	if i == 0:  # 200
		response = current_page.read_file('page.html')
		header = 'Content-Type: text/html'
		content = cms_replace(response['content'], context).encode('utf-8')
	elif i == 1:  # 301
		response = current_page.read_file('redirect-permanent.txt')
		location = cms_replace(response['content'].strip(), context).encode('utf-8')
		header = 'Status: 301 Moved Permanently\nLocation: %s\nContent-Type: text/html' % location
	elif i == 2:  # 302
		response = current_page.read_file('redirect-temporary.txt')
		location = cms_replace(response['content'].strip(), context).encode('utf-8')
		header = 'Status: 302 Moved Temporarily\nLocation: %s\nContent-Type: text/html' % location
	elif i == 3:  # 404
		header = 'Status: 404 Not Found\nContent-Type: text/html'
		content = Resource('error', '404').read_file('page.html')['content']

	print header; print; sys._finishedprintingheader = True
	print content


def cms_replace(content_old, context):
	import re
	content_new = ''; prev_end = 0

	includes = re.finditer(r'(\\?)<?!--\s*%@\s*([\w_-]+)\s*:([^>]*)-->?', content_old, flags=0)
	for include in includes:
		content_new += content_old[prev_end:include.start()]
		backslash = include.group(1)
		if backslash == '\\': content_append = include.group(0)[1:]  # backslash escape
		else:
			keyword = include.group(2); args = include.group(3).strip()
			try:
				include_context, include_content = include_features[keyword](context, args)
				content_append = cms_replace(include_content, include_context)
			except KeyError: content_append = '<!-- include %s not found -->' % repr(keyword)
		try: content_new += content_append
		except UnicodeError: raise UnicodeError(content_new, content_append)
		prev_end = include.end()

	content_new += content_old[prev_end:]
	return content_new

class Resource:
	def __init__(self, kind, name):
		import os.path
		self.kind = kind
		self.name = name
		self._dir = os.path.join('..', kind, name)

	def dir(self, subpath=''):
		import os.path
		return os.path.join(self._dir, subpath)

	def exists_file(self, filename):
		import os.path
		return os.path.exists(self.dir(filename))

	def read_file(self, filename):
		import os.path
		if os.path.exists(self._dir):
			try: content = open(self.dir(filename)).read()
			except IOError, e: return {'status': 404, 'details': '%s: %s' % (e.strerror, e.filename)}
			content = content.decode('utf-8')
			return {'status': 200, 'content': content}
		else: return {'status': 404, 'details': 'page not found'}

def make_includes():

	def include_page(context, page_name):
		context = Resource('pages', page_name)
		response = context.read_file('page.html')
		if response['status'] > 200: return context, '<!-- error including page %s template -- %s: %s -->' % (repr(page_name), response['status'], response['details'])
		return context, response['content']
	def include_html_file(context, filename_no_ext):
		filename = filename_no_ext+'.html'
		response = context.read_file(filename)
		if response['status'] > 200: return context, '<!-- error including html-- %s: %s -->' % (response['status'], response['details'])
		return context, response['content']
	def include_mdown_file(context, filename_no_ext):
		try:
			import markdown2
			filename = filename_no_ext+'.mdown'
			response = context.read_file(filename)
			if response['status'] > 200: return context, '<!-- error including mdown -- %s: %s -->' % (response['status'], response['details'])
			return context, markdown2.markdown(response['content'])
		except ImportError:
			return context, '<!-- error including mdown -- can\'t import module markdown2 -->'
	def include_widget(context, widget_name):
		context = Resource('widgets', widget_name)
		response = context.read_file('widget.html')
		if response['status'] > 200: return context, '<!-- error including widget -- %s: %s -->' % (response['status'], response['details'])
		return context, response['content']
	def include_root(context, blank):
		return context, '/'
	def include_current_page(context, blank):
		return context, page_name.replace('/', '__')
	def include_is_page(context, compared_page_name):
		if page_name == compared_page_name: return context, 'current'
		else: return context, ''
	def include_in_page(context, compared_page_name):
		if page_name.startswith(compared_page_name): return context, 'current'
		else: return context, ''
	def include_server(context, blank):
		import os; return context, os.environ['HTTP_HOST'].replace('.', '_')
	def include_path(context, blank):
		import os; path = os.environ['PATH_INFO'];
		return context, path
	def include_current_url(context, blank):
		import os; path = os.environ['REQUEST_URI'];
		return context, path

	return {
		'page': include_page,
		'widget': include_widget,
		'html': include_html_file,
		'mdown': include_mdown_file,
		'root': include_root,
		'is-page': include_is_page,
		'in-page': include_in_page,
		'server': include_server,
		'current-name': include_current_page,
		'current-path': include_path,
		'current-url': include_current_url,
	}

include_features = make_includes()
page_name = os.environ['PATH_INFO'].lstrip('/')
if page_name == '': page_name = '_'
current_page = Resource('pages', page_name)


execfile('extensions.py')


print_page()
