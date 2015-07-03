from util import controller, Response, Router


@controller
def index(request):
    """
    The first page for visit
    """
    name = request.session.get('name', 'Anonymous')  # for the first entering the visitor is unknown
    return Response(200, "(INDEX PAGE) Hello {who}".format(who=name))


@controller
def hello(request):
    """
    After this page visit index page once more
    and you'll see... magic
    """
    name = 'Anton'
    request.session['name'] = name  # remember the name for the visitor
    return Response(200, "(HELLO PAGE) Hello {who}".format(who=name))

router = Router({
    '/': index,
    '/hello': hello,
})
