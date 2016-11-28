from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve
from django.shortcuts import render, redirect

from .models import *


# helper views

def info(request, messages):
    if type(messages) != 'list':
        messages = [messages]
    return render(request, 'info.html', {'messages': messages})


def error(request, messages):
    if type(messages) != 'list':
        messages = [messages]
    return render(request, 'error.html', {'errors': messages})


# start view

@login_required(login_url='login/')
def index(request):
    """
    Lists all drinks in the system
    and shows current order (cart)
    """
    try:
        account = Account.for_user(request.user)
    except (KeyError, Account.DoesNotExist):
        return error(request, "You have no account. Please, contact with administrator")

    drinks = Drink.objects.order_by('-priority')
    order = account.new_order()
    context = {'drinks': drinks, 'order': order, 'items': order.get_items()}
    return render(request, 'index.html', context)


# order processing

@login_required(login_url='login/')
def order_view(request):
    order = Account.for_user(user=request.user).new_order()
    return render(request, 'order/details.html', {'order': order, 'items': order.get_items()})


@login_required(login_url='login/')
def order_list(request):
    orders = Account.for_user(request.user).list_orders()
    return render(request, 'order/list.html', {'orders': orders})


@login_required(login_url='login/')
def order_add_item(request):
    # process drink
    order = Account.for_user(request.user).new_order()
    drink = OrderItem(order=order)
    drink.product = Product.objects.get(pk=request.GET['product_id'])
    drink.save()

    # process toppings
    if 'toppings' in request.GET:
        for product_id in request.GET.getlist('toppings'):
            print(product_id)
            topping = OrderItem(order=order, parent=drink)
            topping.product = Product.objects.get(id=product_id)
            topping.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login/')
def order_remove_item(request):
    OrderItem.objects.get(pk=request.GET['item_id']).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login/')
def order_checkout(request):
    order = Account.for_user(request.user).new_order()
    order.status = Order.WAITING
    order.save()
    return info(request, 'Thank you. Your order is received')
