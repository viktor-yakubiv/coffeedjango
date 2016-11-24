from django.http import HttpResponse


def index(request):
    return HttpResponse(
        '<!DOCTYPE html>'
        '<title>Coffee bar</title>'
        '<h1>Coffee bar</h1>'
        '<p>Hello, coffee bar visitor</p>'
    )
