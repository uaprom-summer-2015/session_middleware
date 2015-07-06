import uuid
from wsgiref.simple_server import make_server
from example_server import simple_app
from Cookie import SimpleCookie


def reverse_middleware(app):
    def wrapped_app(environ, start_response):
        response = app(environ, start_response)
        return [s[::-1] for s in response]
    return wrapped_app

def session_middleware(app, sessions=dict()):
    def _start_response(func, cookies):
        def wrapper(status_code, headers):
            headers.extend(("set-cookie", morsel.OutputString()) for morsel in cookies.itervalues())
            return func(status_code, headers)
        return wrapper

    def wrapped_app(environ, start_response):
        cookies = SimpleCookie()
        if 'HTTP_COOKIE' in environ:
            cookies.load(environ['HTTP_COOKIE'])

        if 'session_id' not in cookies:

            session_id = str(uuid.uuid4())
            cookies['session_id'] = session_id

        sessions[cookies['session_id'].value] = None  # for additional purposes

        return app(environ, _start_response(start_response, cookies))

    return wrapped_app

if __name__ == '__main__':
    make_server('', 8000, reverse_middleware(simple_app)).serve_forever()
