from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from urllib3 import HTTPResponse
from django.contrib.auth import logout, authenticate,login
from .models import Products,WishList,Cart,Deshboard,DeliveryAddress,PromoCode,Orderitem,productComment,Product_features,sellingProRegistery,notifyYou
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from shop.templatetags import poll_extras
import datetime
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
User = get_user_model()
import json
shippingCharge = 10
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
        user = User.objects.create(email=email, password=userpass)
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
    try:
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
        # Promo Code Offer
        promocode_offer_qry = PromoCode.objects.filter(display_promo=True).values()
        # 

        # Product Feature
        product_feature = Product_features.objects.filter(product_id=params).values()
        #
        permissionScope = False     
        noOfBuyer = set()
        for orderitem in orderQry:
            if orderitem.buyer == request.user:
                permissionScope = True
            noOfBuyer.add(orderitem.buyer)
        #print("reply=====1111111111111111111111===",replyDict)
        total_rating = sum(rating.values())
        overall_productRating = ""
        overall_productRating = round((1*rating['first']+2*rating['second']+3*rating['third']+4*rating['four']+5*rating['five'])/total_rating,1)
    except:
        pass
    obj = {'params': params,'comments':comments,'replies':replyDict,'permissionScope':permissionScope,'noOfBuyer':len(noOfBuyer),'rating':rating,'total_rating':total_rating,'noOfReview':len(qry)+len(replies),'overall_productRating':overall_productRating,'promocode_offer_qry':promocode_offer_qry,'product_feature':product_feature}
    return render(request,'shop/productinfo.html',obj)
        # except:
        #     return HttpResponse("<h1>This Product is not available</h1>")
    return redirect("shop/")
def category(request,search):
    params={"search":search}
    obj = Products.objects.filter(product_Category=search).values()
    number_of_records = 2
    paginator = Paginator(obj,number_of_records)
    page_number = request.GET.get('page')
    obj = paginator.get_page(page_number)
    params = {'pro_data': obj}
    return render(request,'shop/category.html',params)
def cart(request,productid=None):
    if productid:
        if not Cart.objects.filter(Q(buyer=request.user) & Q(product_id=productid)).exists():
            qry = Products.objects.get(product_id = productid)
            Cart(buyer=request.user,product_id=qry).save()
    # Getting All Cart Data For User
    cartQry = Cart.objects.filter(buyer=request.user)
    obj = []
    for i in cartQry:
        if i.product_id.product_quantity != 0:
            if i.product_id.product_quantity < i.quantity:
                i.quantity = i.product_id.product_quantity
            obj.append({'product_id':i.cart_product_id,'product_pic':i.product_id.product_Catelog,'product_Name':i.product_id.product_Name,'product_Actual_Price':int(i.product_id.product_Price),'product_OfferPrice':int(i.product_id.product_OfferPrice),'product_quantity':i.quantity})
            i.save()
    obj1 = {'params':obj,'shipping_Charge':shippingCharge}
    return render(request,'shop/cart.html',obj1)

@csrf_exempt
def cartorderremove(request):
    if request.method == 'POST':
        productid = request.POST.get('productid')
        Cart.objects.get(buyer=request.user,cart_product_id=productid).delete()   
        #Call Variable -> Indicate We want value not in JSONRESPONSE Formate  
        return JsonResponse({'status':True,'param':priceDetailsUpdateSection(request,indicate=True)})

@csrf_exempt
def priceDetailsUpdateSection(request,indicate=None):
    # Getting All Cart Data For User
    Shipping_Charge = shippingCharge
    cartQry = Cart.objects.filter(buyer=request.user)
    obj = []
    for i in cartQry:
        if i.product_id.product_quantity != 0:
            obj.append({'product_Name':i.product_id.product_Name,'product_Actual_Price':int(i.product_id.product_Price),'product_OfferPrice':int(i.product_id.product_OfferPrice),'product_quantity':i.quantity})
    print("length======================",len(obj))
    Shipping_Charge = 0 if len(obj)==0 else Shipping_Charge
    if indicate:
        return {'params':obj,'shipping_Charge':Shipping_Charge,'status':True}
    else:
        return JsonResponse({'params':obj,'shipping_Charge':Shipping_Charge,'status':True})


@csrf_exempt
def cartmodifyquantity(request):
    if request.method == 'POST':
        cartid = request.POST.get('cartid')
        itemQuantity = request.POST.get('itemQuantity')
        status = 'Your Cart Quantity has been added'
        print("Cart Modify Quantity Function Trigger",cartid,itemQuantity)
        cartqry = Cart.objects.get(cart_product_id=cartid)
        print("cartQry===========",cartqry)
        qry = ""
        try:
            qry = Products.objects.get(product_id=cartqry.product_id.product_id,product_quantity__gte=itemQuantity)
            cartqry.quantity = itemQuantity
            cartqry.save()
        except:
            status = 'Input Quantity is not available yet'
    return JsonResponse({'status':status,'param':priceDetailsUpdateSection(request,indicate=True)})

def wishlist(request,productid=None):
    if productid:
        if not WishList.objects.filter(Q(buyer=request.user) & Q(product_id=productid)).exists():
            qry = Products.objects.get(product_id = productid)
            WishList(buyer=request.user,product_id=qry).save()
    # Getting All WishList Data For User
    cartQry = WishList.objects.filter(buyer=request.user)
    obj = []
    for i in cartQry:
        obj.append({'product_id':i.product_id.product_id,'product_pic':i.product_id.product_Catelog,'product_Name':i.product_id.product_Name,'product_Quantity':i.product_id.product_quantity,'product_price':i.product_id.product_OfferPrice})
    obj1 = {'params':obj}
    return render(request,'shop/wishlist.html',obj1)

def checkoutdeliveryaddress(request,productid=None):
    qry = DeliveryAddress.objects.filter(buyer = request.user).values()
    obj = {'params':qry,'productid':productid}
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
        obj = DeliveryAddress(buyer=request.user,deliver_country=country,fullname=fullname,mobileno=mobileno,pincode=pincode,flatno=flatno,area=area,landmark=landmark,city=city,state=state)
        obj.save()
        return JsonResponse({'status': True,'country':country,'fullname':fullname,'mobileno':mobileno,'pincode':pincode,'flatno':flatno,'area':area,'landmark':landmark,'city':city,'state':state,'address_id':obj.address_id})
    else:
        return JsonResponse({"status":False})

def paymentsection(request,productid=None):
    request.session['deliveryAddress'] = ''
    print("productid ================ $$$$$$$$$$$$$$$$$$",productid)
    request.session['deliveryAddress'] = request.POST.get('deliveryaddress')
    print("Delivery Address============",request.session['deliveryAddress'])
    # Getting All Cart Data For User
    obj = []
    request.session['totalpaybleamount'] = 0
    promocode_qry = PromoCode.objects.filter(display_promo=True).values()
    cartflag = True
    if productid:
        cartflag = False
        product_data = Products.objects.get(product_id=productid)
        obj.append({'product_id':product_data.product_id,'product_pic':product_data.product_Catelog,'product_Name':product_data.product_Name,'product_Actual_Price':product_data.product_Price,'product_OfferPrice':product_data.product_OfferPrice})
        request.session['totalpaybleamount'] = request.session['totalpaybleamount'] + product_data.product_OfferPrice
    else:
        cartQry = Cart.objects.filter(buyer=request.user)
        for i in cartQry:
            if i.product_id.product_quantity >=i.quantity:
                print("(i.product_id.product_OfferPrice)*i.quantity",int(i.product_id.product_OfferPrice)*i.quantity)
                print("i.quantity",i.quantity)
                obj.append({'product_id':i.product_id.product_id,'product_pic':i.product_id.product_Catelog,'product_Name':i.product_id.product_Name,'product_Actual_Price':(i.product_id.product_Price)*i.quantity,'product_OfferPrice':(i.product_id.product_OfferPrice)*i.quantity})
                request.session['totalpaybleamount'] = request.session['totalpaybleamount'] + i.product_id.product_OfferPrice*i.quantity
        
    obj1 = {'params':obj,'promocode_qry':promocode_qry,'shipping_Charge':shippingCharge,'cartflag':cartflag}
    return render(request,'shop/paymentsection.html',obj1)

@csrf_exempt
def promocodevalidate(request):
    print("Promo Code Validate ===========")
    date_today = datetime.datetime.now().date()
    if request.method == 'POST':
        promocode = request.POST.get('promocode')
        request.session['promoCode'] = promocode
        qry = PromoCode.objects.get(Q(promocode=promocode) & Q(creationDate__lte=date_today) & Q(enddate__gte=date_today) & Q(min_purchase__lte = request.session['totalpaybleamount']))
         
        print('qry',type(qry),qry.promocode)
        return JsonResponse({'status':'Success','promocode':qry.promocode,'promocodeamt':request.session['totalpaybleamount'] - qry.fixed_amount_off})

def pay(request,productid=None):
    print("##########################",productid)
    product_QuantityFullfill = ''
    productQuantity = 1
    flag = False
    print("productid=======",productid)
    Amount_registery = 0
    OfferAmount_registery = 0
    item_registery = dict()
    if productid:
        print("################!!!!!!!!!!!!!!!!!!!!!!!!!!##########",productid)
        product_qry = Products.objects.get(product_id=productid)
        if product_qry.product_quantity > 0:
            print("request.session['deliveryAddress']",request.session['deliveryAddress'])
            Orderitem(buyer=request.user,product_id=product_qry,order_date=datetime.datetime.now().date(),deliveryAddress= (DeliveryAddress.objects.get(address_id=request.session['deliveryAddress']))).save()
            pro_qry = Products.objects.get(product_id = product_qry.product_id)
            product_qry.product_quantity -=productQuantity
            temp = dict()
            temp['product_id'] = str(pro_qry.product_id)
            temp['product_Name'] = pro_qry.product_Name
            temp['product_OfferPrice'] = pro_qry.product_OfferPrice
            temp['product_quantity'] = productQuantity
            temp['product_Tax_Percent'] = pro_qry.product_Tax_Percent
            item_registery["product1"] = temp
            Amount_registery += pro_qry.product_Price
            OfferAmount_registery += pro_qry.product_OfferPrice

            # items_registery.append(pro_qry.product_id)
            # #amount_registery.append(pro_qry.product_OfferPrice)
            product_qry.save()
        else:
            flag = True
            product_QuantityFullfill+= "  "+product_qry.product_Name
        
    else:
        print("~~~~~~~~~~~~~~~~~")
        qry = Cart.objects.filter(buyer=request.user)
        messages.success(request,"Your Order has been made")
        messages.tags = "success"
        product_QuantityFullfill = "These Products have out of Stock"
        pro_seq = 1
        for item in qry:
            if item.product_id.product_quantity >= item.quantity:
                print('item.product_id.product_quantity >= item.quantity',item.product_id.product_quantity,item.quantity)
                Orderitem(buyer=request.user,product_id=item.product_id,order_date=datetime.datetime.now().date(),quantity=item.quantity,deliveryAddress= (DeliveryAddress.objects.get(address_id=request.session['deliveryAddress']))).save()
                pro_qry = Products.objects.get(product_id = item.product_id.product_id)
                #items_registery.append(pro_qry.product_id)
                #amount_registery.append(pro_qry.product_OfferPrice)
                pro_qry.product_quantity -=item.quantity
                temp = dict()
                temp['product_id'] = str(pro_qry.product_id)
                temp['product_Name'] = pro_qry.product_Name
                temp['product_OfferPrice'] = pro_qry.product_OfferPrice
                temp['product_quantity'] = item.quantity
                temp['product_Tax_Percent'] = pro_qry.product_Tax_Percent
                item_registery[f"product{pro_seq}"] = temp
                Amount_registery += pro_qry.product_Price
                OfferAmount_registery += pro_qry.product_OfferPrice
                pro_seq+=1
                pro_qry.save()
            else:
                print("Flag Executed")
                flag = True
                product_QuantityFullfill+= "  "+item.product_id.product_Name
        qry.delete()  
    print("item_registery===========",item_registery,len(item_registery))
    # Store Value in sellingProRegistery
    sellingProRegistery(buyer=request.user,orderType='Single' if len(item_registery) == 1 else "Multiple",items=json.dumps(item_registery),amount=Amount_registery,paidAmount=OfferAmount_registery,status='paid',coupon=(request.session['promoCode'] if 'promoCode' in request.session else ''),shippingCharge = shippingCharge).save()
    request.session['promoCode'] = ''
        
    # if flag:
    #     return HttpResponse(f"<h1>{product_QuantityFullfill}</h1>")
    return redirect("/shop/order")

def order(request):
    query_arguments = {'buyer':request.user}
    qry = Orderitem.objects.filter(**query_arguments)
    obj = []
    for i in qry:
        obj.append({'product_id':i.product_id.product_id,'product_pic':i.product_id.product_Catelog,'product_Name':i.product_id.product_Name,'order_date':i.order_date,'delivery_status':i.delivery_status,'quantity':i.quantity})
    obj = {'params':obj}
    return render(request,'shop/order.html',obj)

def productCommentSubmission(request):
    if request.method == "POST":
        comment = request.POST.get("comment",'')
        productid = request.POST.get("productid","")
        parentid = request.POST.get("parentid",'')
        print('request.POST.get("parentid")',parentid)
        messages.success(request,"Your Comment has been saved")
        messages.tags = "success"
        if request.POST.get("parentid"):
            print('request.POST.get("parentid")',request.POST.get("parentid"))
            productComment(comment=comment,user=request.user,product_item=Products.objects.get(product_id=productid),parent=productComment.objects.get(sno=request.POST.get("parentid"))).save()
        else:
            productComment(comment=comment,user=request.user,product_item=Products.objects.get(product_id=productid)).save()
        
    return redirect(request.META['HTTP_REFERER'])


def profile(request):
    obj = User.objects.get(username=request.user)
    print(obj.first_name,obj.last_name,obj.phoneno,obj.email)
    return render(request,'shop/profile.html',{'params':obj})

def profileupdate(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname','')
        lastname = request.POST.get('lastname','')
        email = request.POST.get('email','')
        phoneno = request.POST.get('phoneno')

        query = User.objects.get(username=request.user)
        query.first_name=firstname
        query.last_name=lastname
        query.email=email
        query.phoneno=phoneno
        query.save()
        messages.success(request,"Your profile data has been updated")
        messages.tags = "success"
        return redirect(request.META['HTTP_REFERER'])

def notifyyou(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            notifyYou(buyer=request.user,product_item=Products.objects.get(product_id=product_id)).save()
        except:
            pass
        messages.success(request,"We'll notify you, once product comeback")
        messages.tags = "success"
        return redirect(request.META['HTTP_REFERER'])
