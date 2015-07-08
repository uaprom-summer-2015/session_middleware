from util import controller, Response, Router
from session_middleware import sessions


@controller
def index(request):
    return Response(200, "It works!")

@controller
def hello(request):
    name = request.GET.get('name', ["Anonymous"])[0]
    return Response(200, "Hello %s" % name)


@controller
def name_user(request):
    sid = request.sid
    name = sessions.get(sid) or request.POST.get('name',[None])[0]
    sessions.set(sid, name)

    if name:
        return Response(200, hello % name)
    return Response(200, anonymous)

@controller
def bye(request):
    sid = request.sid
    sessions.set(sid, None)
    return Response(200, anonymous)

router = Router({
    '/index': index,
    '/hello': hello,
    '/username': name_user,
    '/bye': bye
})

anonymous = '''
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>User name</title>
</head>
<body>
    <form action="/username" method="post">
        <label>Enter your name:<br>
            <input type="text" name="name"/>
        </label>
        <input type="submit" value='sign in'/>
    </form>
</body>
</html>'''

hello = '''
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>User name</title>
</head>
<body>
    <p>Hello, %s!</p>
    <form action='/bye' method='post'>
        <input type='submit' value='bye'>
    </form>
</body>
</html>'''