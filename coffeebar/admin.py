from django.contrib import admin

from .models import Account, Product, Drink, Addon


admin.site.register(Account)
admin.site.register(Product)
admin.site.register(Drink)
admin.site.register(Addon)
