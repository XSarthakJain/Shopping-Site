from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings
import uuid
from datetime import date
from django.core.validators import MinValueValidator,MaxValueValidator
# For Extending USer Class
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from django_mysql.models import ListCharField
from django.contrib.postgres.fields import JSONField
# # Create your models here.

class User(AbstractUser):
    phoneno = models.IntegerField(default=0)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

class Products(models.Model):
    product_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    product_Catelog = models.ImageField(upload_to='media',default='media/profile.jpg')
    product_Name = models.CharField(max_length=50)
    product_OfferPrice = models.IntegerField()
    product_Price = models.IntegerField()
    product_Company = models.CharField(max_length=50)
    product_Category = models.CharField(max_length=50)
    product_desc = models.CharField(max_length=200)
    product_quantity = models.IntegerField(default=1,validators=[MinValueValidator(0)])
    product_Tax_Percent = models.IntegerField(default=0,validators=[MinValueValidator(0)])

    def __str__(self):
        return self.product_Name
class Product_features(models.Model):
    product_id = models.ForeignKey('Products',on_delete=models.DO_NOTHING)
    product_feature_Name = models.CharField(max_length=200)
    product_feature_Value = models.CharField(max_length=200)
class Cart(models.Model):
    cart_product_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey('Products',on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)


class WishList(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey('Products',on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

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
    address_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
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
    promocode_provider = models.CharField(max_length=200,default='')
    display_promo = models.BooleanField(default=False)

    def __str__(self):
        return self.promocode

class Orderitem(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey('Products',on_delete=models.DO_NOTHING)
    delivery_status = models.BooleanField(default=False)
    order_date = models.DateField()
    quantity = models.IntegerField(default=1)
    deliveryAddress = models.ForeignKey('DeliveryAddress',on_delete=models.DO_NOTHING) 

class productComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product_item = models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])

    # def __str__(self):
    #     return self.comment[0:15] + "..." + "by"+ settings.AUTH_USER_MODEL

class sellingProRegistery(models.Model):

    ordertypelist = (
        ('Single','Single'),
        ('Multiple','Multiple')
    )
    sellingProRegisteryID = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    orderType = models.CharField(max_length=10,choices=ordertypelist)
    date = models.DateTimeField(auto_now_add=True,blank=True)
    coupon = ListCharField(
        base_field=models.CharField(max_length=100),
        size=25,
        max_length=(25 * 101))
    items = JSONField()
    shippingCharge = models.IntegerField(default=0)
    amount = models.FloatField(default=0)
    paidAmount = models.IntegerField(default=0)
    status = models.CharField(max_length=10,choices=(('paid','paid'),('return','return')))







