from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.Userlogin,name="Userlogin"),
    path("loginsubmission",views.loginsubmission,name="loginsubmission"),
    path("signup",views.signup,name="signup"),
    path("registersignup",views.register_signup,name="register_signup"),
    path("logout",views.logout_handle,name="logout_handle"),
    path("productinfo",views.productinfo,name="productinfo"),
    path('category/<search>/',views.category,name="category")
]