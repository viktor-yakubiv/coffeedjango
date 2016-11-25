from django.contrib import admin

from .models import Account, Drink, Addon


admin.site.register(Account)
admin.site.register(Drink)
admin.site.register(Addon)
