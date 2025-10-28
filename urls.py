"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .models import wishlist
from .views import shop_details, remove_item

urlpatterns = [
    path('',views.index),
    path('base/',views.base),
    path('wishlist/<int:id>/',views.wishlist_func,name='wishlist'),
    path('showishlist/', views.wishlist_read),
    path('blog/',views.blog),
    path('blog-details/',views.blog_detail),
    path('checkout/',views.chekout),
    # path('contact/',views.contact),
    path('main/',views.main),
    path('shop-detail/<int:id>/',views.shop_details),
    path('add-to-cart/<int:id>/',shop_details,name='add-to-cart'),
    path('shop-grid/',views.shop_grid),
    path('shoping-cart/',views.shoping),
    path('remove_item/<int:id>/',views.remove_item),
    path('changequantity/<int:id>/',views.changequantity),
    # path('cupcod/<int:id>/', views.cupcod),
    path('remove_items/<int:id>/',remove_item,name="remove-item"),
    path('remove_wishlist/<int:id>/',views.remove_wishlist,name="remove_wishlist"),
    path('signup_func/', views.signup_func),
    path('signin_func/', views.signin_func),
    path('signout_func/', views.signout_func),
    path('contact_func/', views.contact_func),

]
