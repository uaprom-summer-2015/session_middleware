from urlparse import parse_qs
from collections import namedtuple
import Cookie

def Request(environ):
    return namedtuple('Request', ['path', 'GET', 'sid', 'POST'])(
        path=environ['PATH_INFO'],
        GET=parse_qs(environ['QUERY_STRING']),
        sid = Cookie.SimpleCookie(environ.get('HTTP_COOKIE', {})).get('sid').value,
        POST = parse_qs(environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH') or '0'))),
    )

def Response(status, body):
    def wrapper(environ, start_response):
        http_status = {
            200: '200 OK',
            404: '404 Not Found'
        }[status]
        start_response(http_status, [('Content-type', 'text/html')])
        return [body]
    return wrapper

def Router(route_map):
    def router(environ, start_response):
        path = environ['PATH_INFO']
        default = Response(404, 'Page not found')
        action = route_map.get(path, default)
        return action(environ, start_response)
    return router

def controller(func):
    def wrapper(environ, start_response):
         response = func(Request(environ))
         return response(environ, start_response)
    return wrapper
