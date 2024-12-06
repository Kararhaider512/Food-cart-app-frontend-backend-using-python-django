from django.db import models
from django.contrib.auth.models import User


class products(models.Model):
  product_img = models.CharField(max_length=1000)
  product_name=models.CharField(max_length=50)
  product_desc=models.TextField()
  product_price=models.IntegerField()
  
class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
