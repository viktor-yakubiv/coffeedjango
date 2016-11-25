from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from .models import Drink, Account


@login_required(login_url='login/')
def index(request):
    drinks = Drink.objects.order_by('-priority')
    template = loader.get_template('index.html')
    context = {'drinks': drinks}
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def order(request):
    account = Account.objects.get(user=request.user, status=Account.OPENED)
    return HttpResponse(account)

