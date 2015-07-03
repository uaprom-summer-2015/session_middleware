from wsgiref.simple_server import make_server
from middleware import SessionMiddleware
from views import router

make_server('', 8000, SessionMiddleware(router)).serve_forever()
