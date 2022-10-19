from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from urllib3 import HTTPResponse
from django.contrib.auth import logout, authenticate,login


def index(request):
    return render(request,'index.html')
def Userlogin(request):
    return render(request,'login.html')
def loginsubmission(request):
    if request.method == "POST":
        email = request.POST['email']
        userpass = request.POST['userpassword']
        user = authenticate(username=email,password=userpass)
        if user is not None:
            login(request,user)
    return redirect("/")
def signup(request):
    return render(request,'signup.html')
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
        return redirect("/")
    else:
        print("=================================================")
        return HttpResponse("<h1>Logout Module Error<h1>")
