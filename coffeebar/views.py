from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

import os

from .models import *

login_url = reverse_lazy('coffeebar:login')


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

@login_required(login_url=login_url)
def index(request):
    """
    Lists all drinks in the system
    and shows current order (cart)
    """
    try:
        account = Account.for_user(request.user)
    except (KeyError, Account.DoesNotExist):
        if request.user.is_superuser:
            return redirect('coffeebar:admin:accounts:index')
        return error(request, _("You have no account. Please, contact with administrator"))

    drinks = Drink.objects.all().exclude(product__available=False)
    order = account.new_order()
    context = {'drinks': drinks, 'order': order, 'items': order.get_items()}
    return render(request, 'index.html', context)


# order processing

@login_required(login_url=login_url)
def order_details(request, order_id=None):
    context = {}
    account = Account.for_user(request.user)
    if order_id is not None:
        order = Order.objects.get(pk=order_id)
        if order.account != account:
            return error(request, _("Access denied"))
    else:
        order = account.new_order()
    context['edit'] = order.id == account.new_order().id
    context['order'] = order
    context['items'] = order.get_items()
    return render(request, 'order/details.html', context)


@login_required(login_url=login_url)
def order_list(request):
    orders = Account.for_user(request.user).list_orders()
    return render(request, 'order/list.html', {'orders': orders})


@login_required(login_url=login_url)
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


@login_required(login_url=login_url)
def order_remove_item(request):
    OrderItem.objects.get(pk=request.GET['item_id']).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=login_url)
def order_checkout(request):
    order = Account.for_user(request.user).new_order()
    order.status = Order.WAITING
    order.save()
    return info(request, 'Thank you. Your order is received')


@login_required(login_url=login_url)
def admin(request):
    return render(request, 'admin/index.html', {})


@login_required(login_url='coffeebar:login')
def admin_accounts(request, action='list'):
    if action == 'close':
        account = Account.objects.get(pk=request.GET['account_id'])
        account.status = Account.CLOSED
        account.save()
        return redirect('coffeebar:admin:accounts:index')

    if action == 'open':
        user = User.objects.get(pk=request.POST['user_id'])
        if request.POST['password']:
            user.set_password(request.POST['password'])
        user.save()
        account = Account(user=user, owner=request.POST['owner'])
        account.save()
        return redirect('coffeebar:admin:accounts:index')

    context = {
        'active': Account.objects.all().exclude(status=Account.CLOSED),
        'closed': Account.objects.filter(status=Account.CLOSED),

        'users': User.objects.all(),
    }
    return render(request, 'admin/accounts.html', context)


@login_required(login_url=login_url)
def admin_orders(request, action='list'):
    if action == 'update':
        order = Order.objects.get(pk=request.GET['order_id'])
        order.status = min(order.status + 1, Order.DONE)
        order.save()
        return redirect('coffeebar:admin:orders:index')

    context = {
        'undone': Order.objects.filter(account__status=Account.OPENED)
                       .exclude(status=Order.DONE).exclude(status=Order.NEW).order_by('status'),
        'done': Order.objects.filter(account__status=Account.OPENED, status=Order.DONE),
    }
    return render(request, 'admin/orders.html', context)


@login_required(login_url=login_url)
def admin_products(request, action='list', product_id=None):
    context = {}

    if action == 'add':
        product = Product(name=request.GET['name'], price=request.GET['price'])
        if request.GET['image']:
            product.image = request.GET['image']
        product.save()
        if 'drink' in request.GET:
            drink = Drink(product=product)
            drink.save()
        elif 'topping' in request.GET:
            topping = Topping(product=product)
            topping.save()
        return redirect('coffeebar:admin:products:index')

    if action == 'delete':
        Product.objects.get(pk=product_id).delete()
        return redirect('coffeebar:admin:products:index')

    if action == 'toggle':
        product = Product.objects.get(pk=product_id)
        product.available = not product.available
        product.save()
        return redirect('coffeebar:admin:products:index')

    if action == 'edit':
        context['edit'] = Product.objects.get(pk=product_id)

    context['images'] = []
    for static_dir in settings.STATICFILES_DIRS:
        context['images'] += os.listdir(os.path.join(static_dir, 'images/products'))
    context['drinks'] = Drink.objects.all()
    context['toppings'] = Topping.objects.all()
    return render(request, 'admin/products.html', context)
