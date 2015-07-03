from wsgiref.simple_server import make_server

from views import router

make_server('', 8000, router).serve_forever()
