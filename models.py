from tkinter.constants import CASCADE

from django.contrib.auth.models import User
from django.contrib.postgres.operations import TrigramExtension
from django.db import models

# Create your models here.

class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    msg = models.TextField()

class Catagory(models.Model):
    catagory = models.CharField(max_length=50)

    def __str__(self):
        return self.catagory

class Product(models.Model):
    product_img = models.ImageField(upload_to='products')
    cat_name = models.ForeignKey(Catagory, related_name='Category', on_delete=models.CASCADE)
    p_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quntaty = models.IntegerField(default=1)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.p_name


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total =  models.IntegerField(default=0)

    def save(self,*args,**kwargs):
        self.total = self.product.price * int(self.quantity)
        super().save(*args,**kwargs)


class cuponcode(models.Model):
    code = models.CharField(max_length=50,unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)


    def __str__(self):
        return self.code


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    country = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField()
    zip = models.IntegerField()
    phone = models.IntegerField()
    total_amount = models.IntegerField(default=0)
    order_status = models.CharField(max_length=50, default="Pending")
    payment_method = models.CharField(max_length=50, choices=(("Razorpay", "Razorpay"),("Cash on Delivery", "COD"),("paypal","paypal")))
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)


class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
