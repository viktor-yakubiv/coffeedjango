from django.contrib import admin

from .models import Account, Product, Drink, Topping, Order


admin.site.register(Account)
admin.site.register(Product)
admin.site.register(Drink)
admin.site.register(Topping)
admin.site.register(Order)
