#!/usr/bin/python

PATH_WEB_ROOT = '../..'
PATH_TEMPLATES = '../templates'

REDIRECT_PAGES = {
    'redirect.permanently.txt': '301 Moved Permanently',
    'redirect.temporarily.txt': '302 Moved Temporarily',
    'htredirect.301.txt': '301 Moved Permanently',
    'htredirect.302.txt': '302 Moved Temporarily',
}
REDIRECT_WILDCARD_PAGES = {
    'redirect.permanently.wildcard.txt': '301 Moved Permanently',
    'redirect.temporarily.wildcard.txt': '302 Moved Temporarily',
    'htredirect.301.wildcard.txt': '301 Moved Permanently',
    'htredirect.302.wildcard.txt': '302 Moved Temporarily',
}
ERROR_PAGES = {
    '401': '401 Unauthorized',
    '403': '403 Forbidden',
    '404': '404 Not Found',
    '500': '500 Internal Server Error',
    '503': '503 Service Unavailable',
}

PAGE_TEMPLATES = (
    '.htpage.html',
    'htpage.html',
    'page.html',
)

DIR_TEMPLATES = (
    'directory.html',
)


def parse_environment():
    global PAGE, TEMPLATES
    from os import getenv
    PAGE = getenv('REQUEST_URI', '/').lstrip('/').split('?', 1)[0]
    TEMPLATES = path_templates()


def get_http_info():
    from os import getenv
    hostname = getenv('HTTP_HOST', 'localhost')
    https = getenv('HTTPS') == 'on'
    protocol = 'https' if https else 'http'
    host_url = protocol + '://' + hostname
    return {
        'HOSTNAME': hostname,
        'HOST_URL': host_url,
        'HTTPS': https,
    }


def path_web(*path):
    from os.path import join
    return join(PATH_WEB_ROOT, *path)


def path_page(*path):  # not available until PAGE is set
    try:
        return path_web(PAGE, *path)
    except NameError:
        raise RuntimeError('PAGE is unset')


def path_templates(*path):
    from os.path import join
    return join(PATH_TEMPLATES, *path)


def readfile_abs(path):
    f = open(path, 'rb')
    try:
        contents = f.read()
    except IOError:
        f.close()
        raise
    f.close()
    return contents
readfile_web = lambda *path: readfile_abs(path_web(*path))
readfile_page = lambda *path: readfile_abs(path_page(*path))

file_web = lambda *path: file(path_web(*path))
file_page = lambda *path: file(path_page(*path))

from os.path import exists
exists_web = lambda *path: exists(path_web(*path))
exists_page = lambda *path: exists(path_page(*path))


def readtemplate(*path):  # not available until env is set
    try:
        return env.readtemplate(*path)
    except NameError:
        raise RuntimeError('env is unset')


class Status(object):
    '''
    Allows manual setting of status from template: {% do status.set(404) %}
    '''
    def __init__(self):
        self.status = None

    def __nonzero__(self):
        return bool(self.status)

    def __str__(self):
        return str(self.status)

    def __repr__(self):
        return repr(self.status)

    def set(self, value):
        self.status = value
status = Status()


from jinja2 import Environment as JinjaEnvironment


class Environment(JinjaEnvironment):

    @staticmethod
    def create_jinja_env(page, templates_dir, http_info=None):
        global env
        from jinja2 import FileSystemLoader
        env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=FileSystemLoader([
                templates_dir,  # look in site template directory
                path_web(page),  # look in page's directory
                path_web(page, '_'),  # look in '_' subdirectory (useful to keep files from cluttering root)
            ]),
            extensions=[
                'jinja2.ext.do',
            ],
        )
        env.globals.update({
            'env': env,
            'status': status,

            'path_web': path_web,
            'path_page': path_page,
            'readfile_web': readfile_web,
            'readfile_page': readfile_page,
            'file_web': file_web,
            'file_page': file_page,
            'exists_web': exists_web,
            'exists_page': exists_page,
            'readtemplate': env.readtemplate,

            'PAGE': page,
        })
        if http_info:
            env.globals.update(http_info)
        return env

    def readtemplate(env, *path):
        from os.path import join
        return env.get_template(join(*path)).render()

    @staticmethod
    def diff(path, parent):
        if path.startswith(parent):
            return parent, path[len(parent):]
        else:
            raise ValueError('%(path)r does not start with %(parent)r' % locals())

    @classmethod
    def parents(self, path):
        from os.path import split
        head = path
        yield self.diff(path, head)
        head, tail = split(head)
        if not tail:
            head, tail = split(head)
        while True:
            if not (head and tail):
                break
            yield self.diff(path, head)
            head, tail = split(head)

    @classmethod
    def existing_parent(self, page):
        from os.path import exists
        for head, tail in self.parents(page):
            if exists(path_web(head)):
                return head, tail
        return '', page

    @staticmethod
    def parse_redirect_file(*redirect_file):
        return readfile_web(*redirect_file).strip()

    def get_page_redirect(env, page):
        from os.path import join
        for filename in REDIRECT_PAGES:
            if not exists_web(page, filename):
                continue
            location = env.parse_redirect_file(page, filename)
            response = Response()
            response.set_redirect(REDIRECT_PAGES[filename], location)
            return response
        parent, wildcard = env.existing_parent(page)
        for filename in REDIRECT_WILDCARD_PAGES:
            if not exists_web(parent, filename):
                continue
            location = join(env.parse_redirect_file(parent, filename), wildcard)
            response = Response()
            response.set_redirect(REDIRECT_WILDCARD_PAGES[filename], location)
            return response

    def get_page_error(env, page, status_code=None):
        if not status_code:
            from os import getenv
            status_code = getenv('QUERY_STRING')
        if status_code in ERROR_PAGES:
            response = Response()
            template = env.get_template(status_code + '.html')
            response.set_error(ERROR_PAGES[status_code], template.render())
            return response

    def get_page_regular(env, page):
        from jinja2.exceptions import TemplateNotFound
        try:
            template = env.select_template(PAGE_TEMPLATES)
        except TemplateNotFound, exc:
            if exc.name not in PAGE_TEMPLATES:
                raise
            template = env.select_template(DIR_TEMPLATES)
        response = Response()
        response.set_regular(template.render())
        if 'status' in env.globals:
            error_response = env.get_page_error(page, str(env.globals['status']))
            if error_response:
                return error_response
        return response

    def get_page(env, page):
        return env.get_page_redirect(page) or env.get_page_error(page) or env.get_page_regular(page)


class Response(object):

    class ResponseException(Exception):
        pass

    def __init__(self):
        self.header_parts = []
        self.content = None
        self.isfinal = False

    @property
    def header(self):
        return "\n".join(self.header_parts)

    @property
    def content_with_bom(self):
        return u"\uFEFF" + self.content

    #

    def check_final(self):
        if self.isfinal:
            raise self.ResponseException('cannot modify finalized response')

    def append_header(self, line):
        self.check_final()
        self.header_parts.append(line)

    def set_header(self, header):
        self.check_final()
        self.header_parts = None
        self.header = header

    def set_header_status(self, status):
        self.append_header('Status: %s' % status)

    def set_header_location(self, location):
        self.append_header('Location: %s' % location)

    def set_header_content_type(self, content_type):
        self.append_header('Content-Type: %s' % content_type)

    def set_header_html(self):
        self.set_header_content_type('text/html')
        self.is_html = True

    def set_header_plaintext(self):
        self.set_header_content_type('text/plain')
        self.is_html = False

    def set_content(self, content):
        self.check_final()
        self.isfinal = True
        self.content = content

    #

    def set_redirect(self, status, location):
        self.set_header_status(status)
        self.set_header_location(location)
        self.set_header_plaintext()
        self.set_content('Redirecting to: %s' % location)

    def set_error(self, status, content):
        self.set_header_status(status)
        self.set_header_html()
        self.set_content(content)

    def set_regular(self, content):
        self.set_header_status('200 OK')
        self.set_header_html()
        self.set_content(content)

    #

    def print_header(self):
        if not self.header_parts:
            raise self.ResponseException('header is empty')
        print self.header
        print
        import sys
        sys._finishedprintingheader = True

    def print_content(self):
        print self.content_with_bom.encode('utf-8') if self.is_html else self.content
