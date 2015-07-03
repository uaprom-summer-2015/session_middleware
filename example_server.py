from wsgiref.simple_server import make_server

def simple_app(environ, start_response):
    start_response( '200 OK', [('Content-type', 'text/plain')])
    return  ["Hello world"]

if __name__ == '__main__':
    make_server('', 8000, simple_app).serve_forever()
