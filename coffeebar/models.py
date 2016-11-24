from django.db import models
from django.utils import timezone


class User(models.Model):
    room = models.CharField(max_length=10)
    pin = models.CharField(max_length=10)
    name = models.CharField(max_length=150, blank=True)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ' (' + self.room + ')'


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    open_datetime = models.DateTimeField('Opening date and time', default=timezone.now)
    close_datetime = models.DateTimeField('Payment date and time', blank=True)


class Product(models.Model):
    name = models.TextField(max_length=150)
    price = models.FloatField(default=0.0)
    # TODO: add related_to field for nested products
    # related_to = models.ForeignKey(Product, parent_link=True)
    image = models.TextField(max_length=128, blank=True, default='none.png')

    def __str__(self):
        return self.name


class Order(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # TODO: also add related_to field for nested products
    # NOTE: is 'count' field necessary
