from wsgiref.simple_server import make_server
from session_middleware import SessionMiddleware

from views import router

conf = {'storage': 'file',
        'filename': './session.txt'}
make_server('', 8000, SessionMiddleware(router, conf)).serve_forever()
