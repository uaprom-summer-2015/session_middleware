from wsgiref.simple_server import make_server
from example_server import simple_app
def reverse_middleware(app):
    def wrapped_app(environ, start_response):
        response = app(environ, start_response)
        return [s[::-1] for s in response]
    return wrapped_app
if __name__ == '__main__':
    make_server('', 8000, reverse_middleware(simple_app)).serve_forever()
