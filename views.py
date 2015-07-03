from util import controller, Response, Router


@controller
def index(request):
    return Response(200, "It works!")

@controller
def hello(request):
    name = request.GET.get('name', ["Anonymous"])[0]
    return Response(200, "Hello %s" % name)

router = Router({
    '/index': index,
    '/hello': hello,
})
