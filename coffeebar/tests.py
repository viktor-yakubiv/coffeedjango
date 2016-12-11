from random import *
from django.test import TestCase

from .models import *


class OrderTest(TestCase):
    def test_total(self):
        """
        Total should be 0.00 for empty Orders
        """

        # create user
        user = User(username='user')
        user.set_password('password')
        user.save()
        # create user account
        account = Account(user=user)
        account.save()
        # create new order
        order = Order(account=account)
        order.save()

        # test total for zero
        self.assertEqual(order.total(), 0.00, "order.total() error for empty orders")

        # add random items
        total_expected = 0.00
        for i in range(1, randrange(1, 10)):
            product = Product(price=random() * 5)
            product.save()
            item = OrderItem(order=order, product=product, quantity=randint(1, 5))
            item.save()

        # test non-empty order
        self.assertEqual(order.total(), total_expected, "order.total() error for non-empty orders")
