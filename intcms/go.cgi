#!/usr/bin/env python
#!/usr/bin/env python -B

ERROR_TEMPLATE_START = '''
<style>
  #_python_error_%(rand)s, #_python_error_%(rand)s * {
    margin: 0;
    padding: 0;
    border: 0;
    font-size: 100%;
    font: inherit;
    vertical-align: baseline;
  }

  #_python_error_%(rand)s {
    background-color: #ffe;
    border: 1px solid #a10;
    color: #a10;
    float: none;
    font-family: 'Lucida Grande', Tahoma, Arial, serif;
    font-size: 15px;
    max-width: 600px;
    margin: 5px auto;
    padding: 8px;
    text-align: left;
  }

  #_python_error_%(rand)s h3 {
    font-family: Menlo, 'Courier New', monospace;
    font-weight: bold;
    font-size: 12px;
  }

  #_python_error_%(rand)s pre {
    font-family: Menlo, 'Courier New', monospace;
    font-size: 12px;
    white-space: pre-wrap !important;
  }

  #_python_error_details_%(rand)s, ._python_error_details_%(rand)s {
    border-top: 1px solid #a10;
    margin-top: 0.7em;
    padding-top: 0.7em;
  }
</style>
<title>Error</title>
<div id="_python_error_%(rand)s">
  <div onclick="document.getElementById('_python_error_details_%(rand)s').style.display=''">
    An internal server error occured.
  </div>
  <div id="_python_error_details_%(rand)s" class="_python_error_details_%(rand)s" style="display: none;">
'''

ERROR_TEMPLATE_END = '''
  </div>
</div>
'''

try:
    from os import getenv
    if getenv('QUERY_STRING') == 'cprofile':
        import cProfile
        cProfile.run("execfile('main.py')", 'cProfile.out')
    else:
        execfile('main.py')

except:
    import sys
    from cgi import print_exception

    if not getattr(sys, '_finishedprintingheader', False):
        print 'Status: 500 Internal Server Error'
        print 'Content-Type: text/html'
        print

    try:
        import random
        rand = str(random.randint(10000, 99999))
        exc_info = sys.exc_info()
        print ERROR_TEMPLATE_START.replace('%(rand)s', rand)
        print_exception(*exc_info)
        print ERROR_TEMPLATE_END.replace('%(rand)s', rand)

    except:
        print '''<h3>An internal server error occurred:</h3>'''
        print_exception(*exc_info)
        print '''<hr>'''
        print '''<h3>In addition, the server encountered another error while generating the error output:</h3>'''
        exc_info = sys.exc_info()
        print_exception(*exc_info)
