from django.contrib import admin

from .models import Products
from .models import Cart
from .models import WishList

# Register your models here.
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(WishList)