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

    # common fields (for login)
    username = models.CharField('Room number', max_length=8)
    password = models.CharField('PIN Code', max_length=12)

    # meta data
    owner_name = models.CharField(max_length=150, blank=True, null=True)

    # status of account
    #   typically look up only for open accounts
    status = models.IntegerField(choices=(
        (OPENED,    'Opened'),
        (CLOSED,    'Closed'),
        (SUSPENDED, 'Suspended'),
    ))

    def __str__(self):
        return '%s (%s)' % (self.username, self.owner_name if self.owner_name != '' else 'Unknown')


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField(default=0.00)
    image = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return '%s ($%f)' % (self.name, self.price)


class Addon(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)


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
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)

    # group of product with list of variants
    group = models.TextField('Drink group', editable=False, choices=[
        ('Hot Coffee',  'Hot Coffee'),
        ('Cold Coffee', 'Cold Coffee'),
        ('Hot Tea',     'Hot Tea'),
        ('Cold Tea',    'Cold Tea'),
    ])

    # sugar:
    #   priority for sorting: higher on top
    #   image filename for front-end
    priority = models.IntegerField(default=0)

    # addons for the product
    addons = models.ManyToManyField(Addon)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
