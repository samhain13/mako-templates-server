#!/usr/bin/env python
""" 
    Based on Mako-[version]/examples/wsgi/run_wsgi.py.
    Changes marked with # S13:...
"""
import cgi, re, os, posixpath, sys
from mako.lookup import TemplateLookup
from mako import exceptions
from mimetypes import guess_type

root = os.getcwd()
host = "0.0.0.0"          # S13: added this so it can be changed.
port = 5000               # S13: used to be 8000, also changeable.
temp = "/tmp/makoserv"    # S13: where to store cached templates.
dis_ext = ["py"]          # S13: a list of file extensions that should 404.
error_style = 'html'      # select 'text' for plaintext error reporting

lookup = TemplateLookup(directories=[root],
    filesystem_checks=True, module_directory=temp,
    # S13: because we'll be using some UTF-8 characters.
    input_encoding="utf-8", output_encoding="utf-8")

def serve(environ, start_response):
    """serves requests using the WSGI callable interface."""
    fieldstorage = cgi.FieldStorage(
        fp = environ['wsgi.input'],
        environ = environ,
        keep_blank_values = True
    )
    # S13: template context has to be a bit more sensible.
    d = dict()
    d["args"] = dict([(k, getfield(fieldstorage[k])) for k in fieldstorage])
    d["env"] = environ

    uri = environ.get('PATH_INFO', '/')
    if uri.endswith("/"):  # S13: use the index.html if no filename is given.
        uri += 'index.html'
    else:
        uri = re.sub(r'^/$', '/index.html', uri)
    
    if re.match(r'.*\.(html|json)$', uri):    # S13: accept JSON requests.
        try:
            template = lookup.get_template(uri)
            if uri.endswith(".json"):         # S13: include the corrent type.
                start_response("200 OK", [('Content-Type','application/json')])
            else:
                start_response("200 OK", [('Content-Type','text/html')])
            return [template.render(**d)]
        except exceptions.TopLevelLookupException:
            start_response("404 Not Found", [])
            return ["Cant find template '%s'" % uri]
        except:
            if error_style == 'text':
                start_response("200 OK", [('Content-Type','text/plain')])
                return [exceptions.text_error_template().render()]
            else:
                start_response("200 OK", [('Content-Type','text/html')])
                return [exceptions.html_error_template().render()]
    elif re.match(r'.*\.(%s)$' % "|".join(dis_ext), uri):
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return ["File not found."]
    else:
        u = re.sub(r'^\/+', '', uri)
        filename = os.path.join(root, u)
        # S13: if the request is a file, proceed as usual.
        if os.path.isfile(filename):
            # S13: use mimetypes.guess_type.
            mt = guess_type(filename)[0]
            if mt: start_response("200 OK", [('Content-Type', mt)])
            else: start_response("200 OK", [])
            return [file(filename).read()]
        # S13: if the request is a directory, redirect to the index.
        elif os.path.isdir(filename):
            uri += "/"
            start_response("302 Moved Permanently", [("Location", uri)])
            return []
        # S13: if it's neither, respond with a 404.
        else:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return ["File not found."]
 
def getfield(f):
    """convert values from cgi.Field objects to plain values."""
    if isinstance(f, list):
        return [getfield(x) for x in f]
    else:
        return f.value

# S13: there used to be a function guess_type here. Removed that
# and simply replaced it with mimetype.guess_type (see imports).
 
if __name__ == '__main__':
    import wsgiref.simple_server
    # S13: Allow us to change the host (name or IP) and port.
    if len(sys.argv) > 1:
        ipp = sys.argv[1].split(":")
        if len(ipp) == 2:
            host = ipp[0]
            port = int(ipp[1])
    server = wsgiref.simple_server.make_server(host, port, serve)
    print "Server listening on port %d" % port
    server.serve_forever()


