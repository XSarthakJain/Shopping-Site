from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from urllib3 import HTTPResponse
from django.contrib.auth import logout, authenticate,login
from .models import Products,WishList,Cart,Deshboard
from django.db.models import Q

def index(request):
    qry = Deshboard.objects.all().order_by('deshboard__rank')
    obj1 = {}
    for item in qry:
        if item.deshboard.tag not in obj1:
            obj1[item.deshboard.tag] = []
        obj1[item.deshboard.tag].append({'deshboard_TagLine':item.deshboard.tag,'deshboard_Product_Catelog':item.deshboard_Product_Catelog,'deshboard_Product_Name':item.deshboard_Product_Name,'deshboard_Product_Description':item.deshboard_Product_Description,'deshboard_product_URL':item.deshboard_product_URL})
    obj2 = {'params':obj1}
    return render(request,'shop/index.html',obj2)
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
    print("@@@@@@@@@@@@@@@@@@@@@@@",obj)
    params = {'pro_data': obj}
    return render(request,'shop/category.html',params)
def cart(request,productid):
    if not Cart.objects.filter(Q(buyer=request.user) & Q(product_id=productid)).exists():
        qry = Products.objects.get(product_id = productid)
        Cart(buyer=request.user,product_id=qry).save()
    # Getting All Cart Data For User
    cartQry = Cart.objects.filter(buyer=request.user)
    obj = []
    for i in cartQry:
        obj.append({'product_id':i.product_id.product_id,'product_pic':i.product_id.product_Catelog,'product_Name':i.product_id.product_Name,'product_Actual_Price':i.product_id.product_Price,'product_OfferPrice':i.product_id.product_OfferPrice})
    obj1 = {'params':obj,'shipping_Charge':10}
    return render(request,'shop/cart.html',obj1)

def wishlist(request,productid):
    if not WishList.objects.filter(Q(buyer=request.user) & Q(product_id=productid)).exists():
        qry = Products.objects.get(product_id = productid)
        WishList(buyer=request.user,product_id=qry).save()
    # Getting All WishList Data For User
    cartQry = WishList.objects.filter(buyer=request.user)
    obj = []
    for i in cartQry:
        obj.append({'product_id':i.product_id.product_id,'product_pic':i.product_id.product_Catelog,'product_Name':i.product_id.product_Name})
    obj1 = {'params':obj}
    return render(request,'shop/wishlist.html',obj1)

def checkoutdeliveryaddress(request):
    return HttpResponse("checkoutdeliveryaddress")