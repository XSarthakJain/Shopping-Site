from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from urllib3 import HTTPResponse
from django.contrib.auth import logout, authenticate,login
from .models import Products,WishList,Cart,Deshboard,DeliveryAddress,PromoCode,Orderitem,productComment
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from shop.templatetags import poll_extras
import datetime

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
    # if productid:
    #     try:
    params = Products.objects.get(product_id = productid)
    qry = productComment.objects.filter(product_item= params,parent=None)
    comments = []
    rating = {"first":0,"second":0,"third":0,"four":0,"five":0}
    for item in qry:
        if item.rating == 1:
            rating["first"]+=1
        elif item.rating == 2:
            rating["second"]+=1
        elif item.rating == 3:
            rating["third"]+=1
        elif item.rating == 4:
            rating["four"]+=1
        elif item.rating == 5:
            rating["five"]+=1
        
        comments.append({'firstname':item.user.first_name,'lastname':item.user.last_name,'comment':item.comment,'sno':item.sno,'date':item.timestamp,'rating':item.rating})
    replies = productComment.objects.filter(product_item= params).exclude(parent=None)
    replyDict = {}
    for item in replies:
        if item.rating == 1:
            rating["first"]+=1
        elif item.rating == 2:
            rating["second"]+=1
        elif item.rating == 3:
            rating["third"]+=1
        elif item.rating == 4:
            rating["four"]+=1
        elif item.rating == 5:
            rating["five"]+=1
        # print("replyDict==============",item.user.first_name)
        if item.parent.sno not in replyDict.keys():
            replyDict[item.parent.sno] = [{"comment":item.comment,'firstname':item.user.first_name,'lastname':item.user.last_name,'date':item.timestamp,'rating':item.rating}]
        else:
            replyDict[item.parent.sno].append({"comment":item.comment,'firstname':item.user.first_name,'lastname':item.user.last_name,'date':item.timestamp,'rating':item.rating})
    orderQry = Orderitem.objects.filter(product_id=params)  
    permissionScope = False     
    noOfBuyer = set()
    for orderitem in orderQry:
        if orderitem.buyer == request.user:
            permissionScope = True
        noOfBuyer.add(orderitem.buyer)
    #print("reply=====1111111111111111111111===",replyDict)
    total_rating = sum(rating.values())
    obj = {'params': params,'comments':comments,'replies':replyDict,'permissionScope':permissionScope,'noOfBuyer':len(noOfBuyer),'rating':rating,'total_rating':total_rating}
    return render(request,'shop/productinfo.html',obj)
        # except:
        #     return HttpResponse("<h1>This Product is not available</h1>")
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
        if i.product_id.product_quantity != 0:
            obj.append({'product_id':i.product_id.product_id,'product_pic':i.product_id.product_Catelog,'product_Name':i.product_id.product_Name,'product_Actual_Price':i.product_id.product_Price,'product_OfferPrice':i.product_id.product_OfferPrice})
    obj1 = {'params':obj,'shipping_Charge':10}
    return render(request,'shop/cart.html',obj1)

def cartorderremove(request,productid):
    Cart.objects.get(buyer=request.user,product_id=productid).delete()    
    messages.success(request,"Your Cart item has been deleted")
    messages.tags = "success"
    return redirect("/shop")

def wishlist(request,productid):
    if not WishList.objects.filter(Q(buyer=request.user) & Q(product_id=productid)).exists():
        qry = Products.objects.get(product_id = productid)
        WishList(buyer=request.user,product_id=qry).save()
    # Getting All WishList Data For User
    cartQry = WishList.objects.filter(buyer=request.user)
    obj = []
    for i in cartQry:
        obj.append({'product_id':i.product_id.product_id,'product_pic':i.product_id.product_Catelog,'product_Name':i.product_id.product_Name,'product_Quantity':i.product_id.product_quantity})
    obj1 = {'params':obj}
    return render(request,'shop/wishlist.html',obj1)

def checkoutdeliveryaddress(request):
    qry = DeliveryAddress.objects.filter(buyer = request.user).values()
    obj = {'params':qry}
    return render(request,'shop/checkoutdeliveryaddress.html',obj)

@csrf_exempt
def deliveryaddresssubmission(request):
    if request.method == "POST":
        country =  request.POST.get('country','')
        fullname = request.POST.get('fullname')
        mobileno = request.POST.get('mobileno')
        pincode = request.POST.get('pincode')
        flatno =  request.POST.get('flatno')
        area = request.POST.get('area')
        landmark =  request.POST.get('landmark')
        city = request.POST.get('city')
        state  = request.POST.get('state')
        DeliveryAddress(buyer=request.user,deliver_country=country,fullname=fullname,mobileno=mobileno,pincode=pincode,flatno=flatno,area=area,landmark=landmark,city=city,state=state).save()
        return JsonResponse({'status': True,'country':country,'fullname':fullname,'mobileno':mobileno,'pincode':pincode,'flatno':flatno,'area':area,'landmark':landmark,'city':city,'state':state})
    else:
        return JsonResponse({"status":False})

def paymentsection(request):
    # Getting All Cart Data For User
    cartQry = Cart.objects.filter(buyer=request.user)
    obj = []
    request.session['totalpaybleamount'] = 0
    for i in cartQry:
        if i.product_id.product_quantity !=0:
            obj.append({'product_id':i.product_id.product_id,'product_pic':i.product_id.product_Catelog,'product_Name':i.product_id.product_Name,'product_Actual_Price':i.product_id.product_Price,'product_OfferPrice':i.product_id.product_OfferPrice})
            request.session['totalpaybleamount'] = request.session['totalpaybleamount'] + i.product_id.product_OfferPrice
    promocode_qry = PromoCode.objects.filter(display_promo=True).values()
    obj1 = {'params':obj,'promocode_qry':promocode_qry,'shipping_Charge':10}
    return render(request,'shop/paymentsection.html',obj1)

@csrf_exempt
def promocodevalidate(request):
    print("Promo Code Validate ===========")
    date_today = datetime.datetime.now().date()
    if request.method == 'POST':
        promocode = request.POST.get('promocode')
        qry = PromoCode.objects.get(Q(promocode=promocode) & Q(creationDate__lte=date_today) & Q(enddate__gte=date_today) & Q(min_purchase__lte = request.session['totalpaybleamount']))
         
        print('qry',type(qry),qry.promocode)
        return JsonResponse({'status':'Success','promocode':qry.promocode,'promocodeamt':request.session['totalpaybleamount'] - qry.fixed_amount_off})

def pay(request):
    productQuantity = 1
    qry = Cart.objects.filter(buyer=request.user)
    messages.success(request,"Your Order has been made")
    messages.tags = "success"
    product_QuantityFullfill = "These Products have out of Stock"
    flag = False
    for item in qry:
        if item.product_id.product_quantity > 0:
            Orderitem(buyer=request.user,product_id=item.product_id,order_date=datetime.datetime.now().date()).save()
            pro_qry = Products.objects.get(product_id = item.product_id.product_id)
            pro_qry.product_quantity -=productQuantity
            pro_qry.save()
        else:
            print("Flag Executed")
            flag = True
            product_QuantityFullfill+= "  "+item.product_id.product_Name
    qry.delete()    
    if flag:
        return HttpResponse(f"<h1>{product_QuantityFullfill}</h1>")
    return redirect("/shop/order")

def order(request):
    qry = Orderitem.objects.filter(buyer=request.user)
    obj = []
    for i in qry:
        obj.append({'product_id':i.product_id.product_id,'product_pic':i.product_id.product_Catelog,'product_Name':i.product_id.product_Name,'order_date':i.order_date,'delivery_status':i.delivery_status})
    obj = {'params':obj}
    return render(request,'shop/order.html',obj)

def productCommentSubmission(request):
    if request.method == "POST":
        comment = request.POST.get("comment",'')
        productid = request.POST.get("productid","")
        parentid = request.POST.get("parentid",'')
        print('request.POST.get("parentid")',parentid)
        if request.POST.get("parentid"):
            print('request.POST.get("parentid")',request.POST.get("parentid"))
            productComment(comment=comment,user=request.user,product_item=Products.objects.get(product_id=productid),parent=productComment.objects.get(sno=request.POST.get("parentid"))).save()
        else:
            productComment(comment=comment,user=request.user,product_item=Products.objects.get(product_id=productid)).save()
        
    return redirect("/shop")
