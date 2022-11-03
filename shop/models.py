from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings
import uuid
# Create your models here.
class Products(models.Model):
    product_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    product_Catelog = models.ImageField(upload_to='media',default='media/profile.jpg')
    product_Name = models.CharField(max_length=50)
    product_OfferPrice = models.IntegerField()
    product_Price = models.IntegerField()
    product_Company = models.CharField(max_length=50)
    product_Category = models.CharField(max_length=50)
    product_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.product_Name

class Cart(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey('Products',on_delete=models.DO_NOTHING)


class WishList(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey('Products',on_delete=models.DO_NOTHING)

# These Tags will display on Deshboard
class DeshboardTags(models.Model):
    tag = models.CharField(max_length=100)
    rank = models.IntegerField()
    
    def __str__(self):
        return self.tag

class Deshboard(models.Model):
    deshboard = models.ForeignKey('DeshboardTags',on_delete=models.DO_NOTHING) 
    deshboard_Product_Catelog = models.ImageField(upload_to='media/deshboard',default='media/deshboard/product.jpg')
    deshboard_Product_Name = models.CharField(max_length=50)
    deshboard_Product_Description = models.TextField(blank=True, null=True)
    deshboard_product_URL = models.URLField(max_length = 500)

    def __str__(self):
        return self.deshboard_Product_Name

class DeliveryAddress(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    deliver_country = models.CharField(max_length=100)
    fullname = models.CharField(max_length=20)
    mobileno = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    flatno = models.CharField(max_length=250)
    area = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)

    def __str__(self):
        return self.flatno
    

class PromoCode(models.Model):
    creationDate = models.DateField()
    enddate = models.DateField()
    promocode = models.CharField(max_length=100)
    no_of_user = models.IntegerField()
    min_purchase = models.IntegerField()
    fixed_amount_off = models.IntegerField()
    promocode_desc = models.CharField(max_length=200,default='')
    display_promo = models.BooleanField(default=False)

    def __str__(self):
        return self.promocode

