from idlelib.rpc import request_queue

import razorpay
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render,redirect

from app.models import Message

from app.models import Catagory

from app.models import Product

from app.models import Cart

from app.models import cuponcode

from app.models import Checkout,wishlist


# Create your views here.
def index(request):

    p = Product.objects.filter(is_published = True)

    return render(request,'index.html',{'p':p})

def base(request):

    c = Cart.objects.filter(user=request.user)

    cart_sum = sum(item.total for item in c)
    total = request.session.get('cart_total', cart_sum)
    return render(request,'base.html',{'total':total})

def wishlist_func(request,id):

    # items = wishlist.objects.filter(user=request.user)

    product = Product.objects.get(id=id)
    wishlist.objects.get_or_create(user=request.user, product=product)

    # return render(request, 'wishlist.html', {'items': items})
    return redirect('/showishlist')

def wishlist_read(request):
    items= wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})

def blog(request):
    return render(request,'blog.html')

def blog_detail(request):
    return render(request,'blog-details.html')

# def contact(request):
#     return render(request,'contact.html')

def main(request):
    return render(request,'main.html')

def shop_details(request,id):

    rc = Catagory.objects.all()
    p = Product.objects.get(id=id)

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        product = Product.objects.get(id=id)
        user = request.user

        cart_item , created = Cart.objects.get_or_create(user=user,product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        return redirect('/shoping-cart')

    contaxt = { 'rc':rc,
                'p':p
                }

    return render(request,'shop-details.html',contaxt)

def shop_grid(request):
    sg = Catagory.objects.all()

    cid = request.GET.get('catagory')
    if cid:
        sp = Product.objects.filter(cat_name=cid)
    else:
        sp = Product.objects.all()

    if request.GET.get('search'):
        p = request.GET.get('search')
        sp = Product.objects.filter(p_name__icontains = p)

    contaxt = {
        'sg':sg,
        'sp':sp
    }
    return render(request,'shop-grid.html',contaxt)

def shoping(request):


    c = Cart.objects.filter(user=request.user)

    cart_sum = sum(item.total for item in c)
    total = cart_sum

    # Discount Code
    discount = 0

    if request.method == 'POST':
        cupcode1 = request.POST['cuponcode']

        discount = 0

        if cupcode1:
            try:
                c1 = cuponcode.objects.get(code=cupcode1)
                discount = (cart_sum * c1.discount) / 100
                total -= discount

                request.session['discount'] = float(discount)
                request.session['coupon_code'] = cupcode1
                request.session['cart_total'] = float(total)


            except cuponcode.DoesNotExist:

                request.session['discount'] = 0
                request.session['coupon_code'] = ''
                request.session['cart_total'] = float(cart_sum)

            else:
                discount = request.session.get('discount', 0)
                total = request.session.get('cart_total', cart_sum)

    contaxt = {
        'c':c,
        'cart_sum':cart_sum,
        'discount':discount,
        'total': total,
    }

    return render(request,'shoping-cart.html',contaxt)


def chekout(request):

    c = Cart.objects.filter(user=request.user)

    cart_sum = sum(item.total for item in c)
    total = request.session.get('cart_total', cart_sum)
    discount = request.session.get('discount', 0)

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        country = request.POST['country']
        address = request.POST['address']
        city = request.POST['city']
        zip = request.POST['zip']
        phone = request.POST['phone']
        email = request.POST['email']
        payment_method = request.POST['payment']


        cart_sum = sum(item.total for item in c)
        total = cart_sum
        print(total)


        if payment_method == 'razorpay':

            client = razorpay.Client(auth=('rzp_test_ytoQRUzHn3jtXL', 'Sc3eDMyJEuNfGzcf5r5eWiLz'))
            amount_in_paise = total * 100  # Razorpay requires amount in paise
            razorpay_order = client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'payment_capture': 1
            })

            Checkout.objects.create(user=request.user,fname=fname, lname=lname, country=country, address=address, city=city,zip=zip,phone=phone, email=email,total_amount=total,payment_method="Razer Pay",order_status="Success", razorpay_order_id= razorpay_order['id'])


            contaxt = {
                'c': c,
                'cart_sum': cart_sum,
                'discount': discount,
                'total': total,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key': 'rzp_test_ytoQRUzHn3jtXL',
                'currency': 'INR'
            }

            c.delete()
            return  redirect('/')
        else:

            check = Checkout.objects.create(user=request.user,fname=fname, lname=lname, country=country, address=address, city=city,zip=zip,phone=phone, email=email,total_amount=total,payment_method="Cash On Delevery",order_status="Success")
            c.delete()

            return redirect('/')


    contaxt = {
        'c': c,
        'cart_sum': cart_sum,
        'discount': discount,
        'total': total,
        'razorpay_key': 'rzp_test_ytoQRUzHn3jtXL',
        'currency': 'INR'
    }


    return render(request, 'checkout.html',contaxt)



def changequantity(request,id):
    
    q = Cart.objects.get(id=id)
    quan = request.POST['quantity']

    if q.quantity == 0:
        q.delete()
        return redirect('/shoping-cart')
    else:
        q.quantity = quan
        q.total = q.total * int(quan)
        q.save()
        return redirect('/shoping-cart')



def remove_item(request,id):
    ri = Cart.objects.get(id=id)
    ri.delete()

    return redirect('/shoping-cart')

def remove_wishlist(request,id):
    rw = wishlist.objects.get(id=id)
    rw.delete()

    return redirect('/showishlist')

def signup_func(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=fname):
            messages.error(request,'Username Already Exists !!')
            return redirect('/signup_func')

        if User.objects.filter(email=email):
            messages.error(request, 'Email Already Exists !!')
            return redirect('/signup_func')

        if pass1 != pass2 :
            messages.error(request,'Passwoard Didnot Match')


        myuser = User.objects.create_user(username=fname, email=email, password= pass1)
        myuser.save()

        subject = "Ogani Project Demo"
        message =  "Hello " + " " + myuser.username + " \n" + "Welcome To Our Project \n" +  "Thenk you for visiting "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        return redirect('/signin_func')
    return render(request,'signup.html')

def signin_func(request):

    if request.method == 'POST':
        username =  request.POST.get('username')
        print(username,'aaaa')
        # email = request.POST.get('email')
        # print(email, 'bbbbb')
        password = request.POST.get('password')
        print(password,'bbbbb')

        user = authenticate(username=username,password=password)
        print(user,'userrrr')

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,'Bed Request !!')
            return redirect('/signin_func')
    return render(request,'signin.html')


def signout_func(request):
    logout(request)
    messages.success(request,'Logged out Sucessfully !!!!')

    return redirect('/')


def contact_func(request):

    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        msg = request.POST['msg']

        m = Message.objects.create(name=name,email=email,msg=msg)

        return redirect('/contact_func ')
    return render(request,'contact.html')


