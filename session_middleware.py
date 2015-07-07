import Cookie
import uuid
import shelve
import os


sessions = shelve.open(os.path.join(os.path.dirname(__file__), 'sessions'))

def session_middleware(app):
    def wrapped_app(environ, start_response):

        cookies = Cookie.SimpleCookie(environ.get('HTTP_COOKIE', {}))
        if 'sid' not in cookies:
            sid = str(uuid.uuid4())
            cookies['sid'] = sid
            sessions[sid] = None

            def wrapped_start_response(status_code, headers):
                    headers.append(('set-cookie', 'sid=%s' % sid))
                    return start_response(status_code, headers)

            return app(environ, wrapped_start_response)

        return app(environ, start_response)

    return wrapped_app
