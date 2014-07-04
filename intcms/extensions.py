#!/usr/bin/env python

# This file shows some ways intcms can be extended. Note that the yaml and markdown modules are
# required for the corresponding features.
# TODO separate individual extensions into files
# TODO dirinfo and pathinfo need to be waaay less ugly


def make_globals():

    #

    def yaml(filename):
        from intcms import file_page
        from yaml import load
        file = file_page(filename)
        return load(file)

    #

    def mdfile(filename, *args, **kwargs):
        """
        Parse text with markdown library.

        :param filename:   - name of file for parsing;
        :param args:       - markdown arguments (http://freewisdom.org/projects/python-markdown/Using_as_a_Module);
        :param kwargs:     - markdown keyword arguments (http://freewisdom.org/projects/python-markdown/Using_as_a_Module);
        :return:           - parsed result.
        """
        from markdown import markdown
        from intcms import readtemplate
        text = readtemplate(filename)
        return markdown(text, *args, **kwargs)

    #

    meta = {}

    def set_meta(property, value):
        if not property in meta:  # let templates override parent templates
            meta[property] = value

    #

    def year():
        import time
        return time.strftime("%Y")
    year = year()

    #

    class pathinfo(object):
        def __init__(self):
            self.generated = False
            self.generated_breadcrumbs = False

        @property
        def filename(self):
            from intcms import PAGE
            from os.path import split
            return split(PAGE.rstrip('/'))[1]

        @property
        def parents(self):
            self.update_parents()
            return self._parents

        def update_parents(self):
            from intcms import PAGE, readfile_web
            breadcrumbs = show_breadcrumbs
            if self.generated and not (breadcrumbs and not self.generated_breadcrumbs):
                return

            parent = PAGE
            from os.path import join, split

            def appendtoparents(path, tail, addslash):
                entry = {
                    'path': path,
                    'tail': tail + '/'*addslash,
                    'tailhtml': ("<span>%s</span>" % tail if tail else '') + '<span class="slash">/</span>'*addslash
                }
                if breadcrumbs:  # assumes root of `path` is webroot
                    try:
                        breadcrumb = readfile_web(parent, 'htbreadcrumb.txt')
                    except IOError:
                        breadcrumb = None  # tail
                    entry['breadcrumb'] = breadcrumb
                parents.append(entry)

            path = join('/', parent)

            parents = []
            base, tail = split(path)
            if tail:
                appendtoparents(path, tail, False)
            path = base
            while True:
                base, tail = split(path)
                appendtoparents(path, tail, True)
                if tail == '':
                    break
                path = base
            parents.reverse()

            self._parents = parents
    pathinfo = pathinfo()
    show_breadcrumbs = True

    #

    class dirinfo():
        def __init__(self):
            self.generated = False

        @staticmethod
        def matches(patterns, string, flags=0):
            from re import match
            for pattern in patterns:
                if match(pattern, string, flags):
                    return True
            else:
                return False

        @property
        def is404(self):
            self.update()
            return self._is404

        @property
        def is403(self):
            self.update()
            return self._is403

        @property
        def filesloaded(self):
            self.update()
            return self._filesloaded

        @property
        def files(self):
            self.update()
            return self._files

        def update(self):
            from intcms import path_page, status
            if self.generated:
                return
            relpath = '.'

            # SPECIAL_FILES = [r'\.', r'ht\w+\.(cgi|html)$', r'index.\w+$', r'ls(.\w+)?$', r'.*\.py[cod]$', r'__pycache__$']
            SPECIAL_FILES = [r'\.', r'ht\w+\.(cgi)$', r'index.\w+$', r'ls(.\w+)?$', r'.*\.py[cod]$', r'__pycache__$']
            from os import listdir
            from os.path import isdir, join

            cwd = path_page(relpath)
            self._filesloaded = False
            self._is404 = False
            self._is403 = False
            filesinfo = None
            try:
                fileslist = listdir(cwd)
                self._filesloaded = True
            except OSError, exc:
                if exc.errno in (2, 20):
                    self._is404 = True
                elif exc.errno is 13:
                    self._is403 = True
                else:
                    raise
            else:
                filesinfo = []
                fileslist.sort()

                for filename in fileslist:
                    filepath = join(cwd, filename)
                    filesinfo.append({
                        'isspecial': self.matches(SPECIAL_FILES, filename),
                        'name': filename,
                        'path': filepath,
                        'isdir': isdir(filepath),
                    })

            if self._is404:
                status.set(404)
            elif self._is403:
                status.set(403)
            self._files = filesinfo
            self.generated = True
    dirinfo = dirinfo()

    return locals()


def make_filters():

    def md(text, *args, **kwargs):
        """
        Parse text with markdown library.

        :param text:   - text for parsing;
        :param args:   - markdown arguments (http://freewisdom.org/projects/python-markdown/Using_as_a_Module);
        :param kwargs: - markdown keyword arguments (http://freewisdom.org/projects/python-markdown/Using_as_a_Module);
        :return:       - parsed result.
        """
        from markdown import markdown
        result = markdown(text, *args, **kwargs)
        if result.startswith('<p>') and result.endswith('</p>'):
            result = result[3:-4]
        return result

    return locals()

from intcms import env
env.globals.update(make_globals())
env.filters.update(make_filters())
