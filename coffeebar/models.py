from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Account(models.Model):
    # account types
    OPENED = 0
    CLOSED = 1
    SUSPENDED = 2

    # owner of account
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # status of account
    #   typically look up only for open accounts
    status = models.IntegerField(choices=(
        (OPENED,    'Opened'),
        (CLOSED,    'Closed'),
        (SUSPENDED, 'Suspended'),
    ))

    def __str__(self):
        display_name = 'Unknown'
        if self.user.first_name or self.user.last_name:
            display_name = (self.user.first_name + ' ' + self.user.last_name).strip()
        return '%s (%s)' % (self.user.username, display_name)


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField(default=0.00)
    image = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return '%s ($%1.2f)' % (self.name, self.price)


class Addon(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    # order statuses
    NEW = 0
    PROCESSING = 1
    DONE = 2

    # fields
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=NEW, choices=(
        (NEW, 'New'),
        (PROCESSING, 'Processing'),
        (DONE, 'Done')
    ))


class Drink(models.Model):
    # drink groups
    categories = [
        ('Hot Coffee',  'Hot Coffee'),
        ('Cold Coffee', 'Cold Coffee'),
        ('Hot Tea',     'Hot Tea'),
        ('Cold Tea',    'Cold Tea'),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)

    # group of product with list of variants
    category = models.TextField('Drink group', editable=False, choices=categories)

    # sugar:
    #   priority for sorting: higher on top
    #   image filename for front-end
    priority = models.IntegerField(default=0)

    # addons for the product
    addons = models.ManyToManyField(Addon, blank=True)

    def __str__(self):
        return str(self.product)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s: %d (%1.2f)' % (self.product.name, self.quantity, self.quantity * self.product.price)
