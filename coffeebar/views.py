from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader


@login_required(login_url='login/')
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def login(request):
    pass
