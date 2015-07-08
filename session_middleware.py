import Cookie
import uuid
import shelve
import os
from collections import namedtuple


sessions_backend = namedtuple('sessions_backend', ['get', 'set',])

def shelve_sessions():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(root_dir, 'shelve')
    sh = shelve.open(path, writeback=True)

    def get(sid, default=None):
        return sh.get(sid, default)

    def set(sid, value):
        sh[sid] = value
        sh.sync()

    return sessions_backend(get, set)


sessions = shelve_sessions()


def session_middleware(app):
    def wrapped_app(environ, start_response):

        cookies = Cookie.SimpleCookie(environ.get('HTTP_COOKIE', {}))
        if 'sid' not in cookies:
            sid = str(uuid.uuid4())
            cookies['sid'] = sid
            sessions.set(sid, None)

            def wrapped_start_response(status_code, headers):
                    headers.append(('set-cookie', 'sid=%s' % sid))
                    return start_response(status_code, headers)

            return app(environ, wrapped_start_response)

        return app(environ, start_response)

    return wrapped_app
