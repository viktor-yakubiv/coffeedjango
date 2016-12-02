from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone


class Account(models.Model):
    # account types
    OPENED = 0
    CLOSED = 1
    SUSPENDED = 2

    # owner of account
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.CharField(max_length=254)

    # status of account
    #   typically look up only for open accounts
    status = models.IntegerField(default=OPENED, choices=(
        (OPENED, 'Opened'),
        (CLOSED, 'Closed'),
        (SUSPENDED, 'Suspended'),
    ))

    def __str__(self):
        return '%s (%s)' % (self.user.username, self.owner)

    @staticmethod
    def for_user(user):
        return Account.objects.get(user=user, status=Account.OPENED)

    def new_order(self):
        try:
            return Order.objects.get(account=self, status=Order.NEW)
        except (KeyError, Order.DoesNotExist):
            order = Order(account=self, status=Order.NEW)
            order.save()
            return order

    def list_orders(self):
        try:
            return Order.objects.filter(account=self).order_by('-datetime')
        except (KeyError, Order.DoesNotExist):
            return []

    def total(self):
        total = OrderItem.objects.filter(order__account=self).aggregate(Sum('product__price'))['product__price__sum']
        return total if total else 0.00


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField(default=0.00)
    image = models.CharField(max_length=128, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return '%s ($%1.2f)' % (self.name, self.price)


class Topping(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.product)


class Drink(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    toppings = models.ManyToManyField(Topping, blank=True)

    # priority for sorting: higher on top
    priority = models.IntegerField(default=0)

    def __str__(self):
        return str(self.product)

    def get_toppings(self):
        return self.toppings.all()


class Order(models.Model):
    # order statuses
    NEW = 0
    WAITING = 1
    PROCESSING = 2
    DONE = 3

    # fields
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=NEW, choices=(
        (NEW, 'New'),
        (WAITING, 'Waiting'),
        (PROCESSING, 'Processing'),
        (DONE, 'Done')
    ))

    def __str__(self):
        return '%d from %s' % (self.id, self.datetime)

    def get_items(self):
        return OrderItem.objects.filter(order=self, parent=None)

    def total(self):
        order_total = OrderItem.objects.filter(order=self).aggregate(Sum('product__price'))['product__price__sum']
        return order_total if order_total else 0.00


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    parent = models.ForeignKey('self', blank=True, null=True)

    def __str__(self):
        return '%s: %d (%1.2f)' % (self.product.name, self.quantity, self.quantity * self.product.price)

    def get_related(self):
        try:
            related = OrderItem.objects.filter(parent=self)
        except (KeyError, OrderItem.DoesNotExist):
            related = []
        return related

    def total(self):
        toppings_price = self.get_related().aggregate(Sum('product__price'))['product__price__sum']
        return self.quantity * (self.product.price + (toppings_price if toppings_price else 0.00))
