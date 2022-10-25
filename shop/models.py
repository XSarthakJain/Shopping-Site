from django.db import models
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