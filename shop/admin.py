from django.contrib import admin

from .models import User
admin.site.register(User)

from .models import Products
from .models import Cart
from .models import WishList
from .models import DeshboardTags
from .models import Deshboard
from .models import DeliveryAddress
from .models import PromoCode
from .models import Orderitem
from .models import productComment
from .models import Product_features
from .models import sellingProRegistery
# Register your models here.
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(WishList)
admin.site.register(DeshboardTags)
admin.site.register(Deshboard)
admin.site.register(DeliveryAddress)
admin.site.register(PromoCode)
admin.site.register(Orderitem)
admin.site.register(productComment)
admin.site.register(Product_features)
admin.site.register(sellingProRegistery)