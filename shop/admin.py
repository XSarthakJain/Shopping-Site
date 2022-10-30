from django.contrib import admin

from .models import Products
from .models import Cart
from .models import WishList
from .models import DeshboardTags
from .models import Deshboard

# Register your models here.
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(WishList)
admin.site.register(DeshboardTags)
admin.site.register(Deshboard)