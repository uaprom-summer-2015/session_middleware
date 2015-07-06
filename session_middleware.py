from wsgiref.simple_server import make_server
from example_server import simple_app
from Cookie import SimpleCookie
import uuid


def session_middleware(app, sessions=dict()):
    def cookies_extension(func, cookies):
        def extension(status_code, headers):
            headers.extend(('set-cookie', cookie.OutputString())
                           for cookie in cookies.itervalues())
            return func(status_code, headers)
        return extension

    def wrapped_app(environ, start_response):
        cookies = SimpleCookie()
        if 'HTTP_COOKIE' in environ:
            cookies.load(environ['HTTP_COOKIE'])
        if 'sid' not in cookies:
            sid = str(uuid.uuid4())
            cookies['sid'] = sid
        sessions[cookies['sid'].value] = None
        return app(environ, cookies_extension(start_response, cookies))
    return wrapped_app


if __name__ == '__main__':
    make_server('', 8000, session_middleware(simple_app)).serve_forever()
