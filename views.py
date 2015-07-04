from util import controller, Response, Router


@controller
def index(request):
    session = request.environ['session']
    name = request.GET.get('name', [session.get('name') or 'Anonymous'])[0]
    return Response(200, "%s, it works!\nUse this link to change your name: /set_name?name=<name>" % name)

@controller
def hello(request):
    session = request.environ['session']
    name = request.GET.get('name', [session.get('name') or 'Anonymous'])[0]
    return Response(200, "Hello %s" % name)

@controller
def set_name(request):
    session = request.environ['session']
    name = request.GET.get('name', [session.get('name') or 'Anonymous'])[0]
    if name == '<name>':
        name = 'Anonymous'
    session.set('name', name)
    return Response(200, "Name is changed to %s" % name)

router = Router({
    '/': index,
    '/index': index,
    '/hello': hello,
    '/set_name': set_name,
})
