from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from urllib3 import HTTPResponse
from django.contrib.auth import logout, authenticate,login
from .models import Products,WishList,Cart


def index(request):
    return render(request,'shop/index.html')
def Userlogin(request):
    return render(request,'shop/login.html')
def loginsubmission(request):
    if request.method == "POST":
        email = request.POST['email']
        userpass = request.POST['userpassword']
        user = authenticate(username=email,password=userpass)
        if user is not None:
            login(request,user)
    return redirect("/shop")
def signup(request):
    return render(request,'shop/signup.html')
def register_signup(request):
    email = request.POST['username']
    userpass = request.POST['userpassword']
    fname = request.POST['fname']
    lname = request.POST['lastname']
    mobile = request.POST['mobileNo']

    # Check Username Alredy Present Or Not
    if not User.objects.filter(username=email).exists():
        print("=============",email,userpass,fname,lname,mobile)
        user = User.objects.create_user(email, email, userpass)
        user.first_name = fname
        user.last_name = lname
        user.save()
        return HttpResponse("<h1>You are Successfully Logged In")
    else:
        return HttpResponse("<h1>This Username is already Present<h1>")
def logout_handle(request):
    if request.method == "POST":
        print("==============")
        logout(request)
        return redirect("/shop")
    else:
        print("=================================================")
        return HttpResponse("<h1>Logout Module Error<h1>")




# Create your views here.
def productinfo(request,productname,productid):
    if productid:
        print("ProductID",productid,productname)
        try:
            qry = Products.objects.filter(product_id = productid).values()
            print("===================Valuesssssssssssss",qry)
            params = {'param':qry}
            return render(request,'shop/productinfo.html',params)
        except:
            return HttpResponse("<h1>This Product is not available</h1>")
    return redirect("shop/")
def category(request,search):
    params={"search":search}
    obj = Products.objects.filter(product_Category=search).values()
    params = {'pro_data': obj}
    return render(request,'shop/category.html',params)
def cart(request,productid):
    qry = Products.objects.get(product_id = productid)
    Cart(buyer=request.user,product_id=qry).save()

   
    return render(request,'shop/cart.html')

def wishlist(request,productid):
    qry = Products.objects.get(product_id = productid)
    WishList(buyer=request.user,product_id=qry).save()
    return render(request,'shop/wishlist.html')