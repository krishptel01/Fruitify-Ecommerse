from django.contrib import admin

from .models import *



# Register your models here.
admin.site.register(Message)
admin.site.register(Catagory)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(cuponcode)
admin.site.register(Checkout)