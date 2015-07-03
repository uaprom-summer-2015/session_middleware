import hashlib
import time
import cPickle
from config import SESSION_FILE


class SessionMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def wrapped_start_response(status, headers):
            sid, new_sid = environ['SID']
            if new_sid:
                headers.append(('Set-Cookie', "SID={sid}".format(sid=sid)))
            return start_response(status, headers)

        string_cookie = environ.get('HTTP_COOKIE', '')
        cookie = self.parse_cookie(string_cookie)
        if 'SID' not in cookie:
            self.sid = self.create_sid()
            environ['SID'] = (self.sid, 1)  # new SID: need to send Set-Cookie
        else:
            self.sid = cookie['SID']
            environ['SID'] = (self.sid, 0)  # 'old' SID: need NOT to send Set-Cookie

        environ['SESSION'] = {}
        response = self.app(environ, wrapped_start_response)
        print environ['SID']
        self.set(environ['SID'][0], environ['SESSION'])

        return response

    @staticmethod
    def parse_cookie(string):
        if not string:
            return {}

        cookie_list = string.split('; ')
        return {couple.split('=')[0]: couple.split('=')[1] for couple in cookie_list}

    @staticmethod
    def create_sid():
        return hashlib.sha1(repr(time.time())).hexdigest()

    @staticmethod
    def get(sid, session):
        """
        JUST FOR EXAMPLE
        """
        with open(SESSION_FILE, 'r+') as session_file:
            for line in session_file:
                components = line.split(':')
                if components[0] == sid:
                    session.update(cPickle.loads(components[1]))
        return session

    @staticmethod
    def set(sid, session):
        """
        JUST FOR EXAMPLE
        """
        with open(SESSION_FILE, 'w') as session_file:
            session_file.write(
                "{sid}:{session}".format(sid=sid, session=cPickle.dumps(session, 1))
            )
