from collections import namedtuple
import fileinput
import os
import pickle
from urlparse import parse_qs
import Cookie
import uuid

__author__ = 's.taran'


class SessionMiddleware(object):
    def __init__(self, app, conf=None):
        self.app = app
        self.conf = conf

    def __call__(self, environ, start_response):
        def session_start_response(status, headers):
            session = environ['session']
            if session.is_new:
                headers.append(('Set-cookie', 'sid=%s' % session.sid))
            return start_response(status, headers)

        cookies = self.get_cookies(environ)
        sid = cookies.get('sid', None)
        sid = sid.value if sid else None
        environ['session'] = Session(sid, self.conf)
        return self.app(environ, session_start_response)

    @staticmethod
    def get_cookies(environ):
        cookie = Cookie.SimpleCookie()
        if 'HTTP_COOKIE' in environ:
            cookie.load(environ['HTTP_COOKIE'])
        return cookie


class SessionStorage():
    __data = {}

    def __init__(self, *args, **kwargs):
        pass

    def load(self, sid):
        return self.__class__.__data.get(sid, {})

    def save(self, data, sid):
        self.__class__.__data[sid] = data


class SessionFileStorage():

    def __init__(self, filename, *args,  **kwargs):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.realpath(os.path.join(dir_path, filename))

        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))

        if not os.path.exists(self.file_path):
            open(self.file_path, 'a').close()

    def load(self, sid):
        with open(self.file_path, 'r+') as handle:
            for line in handle:
                id, data = line.split('#')
                if id == sid:
                    return pickle.loads(data)
        return {}

    def save(self, data, sid):
        new_line = "%s#%s" % (sid, pickle.dumps(data, 2))
        for line in fileinput.input(self.file_path, inplace=True):
            id, old_data = line.split('#')
            if id != sid or not line.strip():
                print line,
        fileinput.close()
        with open(self.file_path, 'a') as handle:
            handle.write(new_line+'\n')


class Session(object):
    storage = {'memory': SessionStorage,
               'file': SessionFileStorage}

    def __init__(self, sid=None, conf=None):
        conf = conf or {}
        self.__sid = sid or self.new_sid()
        self.is_new = sid is None
        self.__storage = Session.storage[conf.get('storage', 'memory')](**conf)
        self.__data = self.__storage.load(self.__sid)

    @property
    def sid(self):
        return self.__sid

    def get(self, name):
        return self.__data.get(name, None)

    def set(self, name, value):
        self.__data[name] = value
        self.__storage.save(self.__data, self.__sid)

    @staticmethod
    def new_sid():
        return str(uuid.uuid1()).replace('-', '')

