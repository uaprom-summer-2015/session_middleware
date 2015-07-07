from wsgiref.simple_server import make_server

from session_middleware import session_middleware
from views import router

make_server('', 8000, session_middleware(router)).serve_forever()
