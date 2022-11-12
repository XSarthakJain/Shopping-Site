from django.urls import URLPattern, path,re_path
from . import views
from django.contrib.staticfiles.urls import static
from django.conf import settings
import re
urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.Userlogin,name="Userlogin"),
    path("loginsubmission",views.loginsubmission,name="loginsubmission"),
    path("signup",views.signup,name="signup"),
    path("registersignup",views.register_signup,name="register_signup"),
    path("logout",views.logout_handle,name="logout_handle"),
    path("productinfo/<productname>/<productid>",views.productinfo,name="productinfo"),
    path('category/<search>/',views.category,name="category"),
    path('cart/<productid>',views.cart,name="cart"),
    path('cartmodifyquantity',views.cartmodifyquantity,name='cartmodifyquantity'),
    path('wishlist/<productid>',views.wishlist,name="wishlist"),
    re_path('^checkout/deliveryaddress/(?P<productid>[a-zA-Z0-9!@#$&()\\-`_.+,/\"]*)',views.checkoutdeliveryaddress,name="checkoutdeliveryaddress"),
    path('deliveryaddresssubmission',views.deliveryaddresssubmission,name="deliveryaddresssubmission"),
    re_path('^checkout/paymentsection/(?P<productid>[a-zA-Z0-9!@#$&()\\-`_.+,/\"]*)',views.paymentsection,name="paymentsection"),
    path('checkout/promocodevalidate',views.promocodevalidate,name="promocodevalidate"),
    re_path('^checkout/pay/(?P<productid>[a-zA-Z0-9!@#$&()\\-`_.+,/\"]*)',views.pay,name="pay"),
    path('order',views.order,name="order"),
    path('cartorderremove/<productid>',views.cartorderremove,name="cartorderremove"),
    path('productCommentSubmission',views.productCommentSubmission,name="productCommentSubmission")


]
