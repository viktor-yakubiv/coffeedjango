from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import *


def error(request, messages):
    if type(messages) != 'list':
        messages = [messages]
    return render(request, 'error.html', {'errors': messages})


@login_required(login_url='login/')
def index(request):
    """
    Lists all drinks in the system
    and shows current order (cart)
    """
    try:
        account = Account.objects.get(user=request.user)
    except (KeyError, Account.DoesNotExist):
        return error(request, "You have no account. Please, contact with administrator")

    drinks = Drink.objects.order_by('-priority')
    order = account.get_active_order()
    if not order:
        order = Order(account=account, status=Order.NEW)
        order.save()

    context = {'drinks': drinks, 'order': order}
    return render(request, 'index.html', context)


@login_required(login_url='login/')
def list_orders(request):
    account = Account.objects.get(user=request.user, status=Account.OPENED)
    try:
        orders = Order.objects.get(account=account)
    except (KeyError, Order.DoesNotExist):
        orders = []
    return render(request, 'index.html', {'orders': orders})


@login_required(login_url='login/')
def add_item(request):
    account = Account.objects.get(user=request.user)
    order = account.get_active_order()

    item = OrderItem(order=order)
    item.product = Product.objects.get(id=request.POST['product_id'])
    item.save()
    return redirect('index')


def checkout(request):
    pass
