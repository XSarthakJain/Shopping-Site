from django.urls import URLPattern, path
from . import views
from django.contrib.staticfiles.urls import static
from django.conf import settings
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
    path('wishlist/<productid>',views.wishlist,name="wishlist"),
    path('checkout/deliveryaddress',views.checkoutdeliveryaddress,name="checkoutdeliveryaddress"),
    path('deliveryaddresssubmission',views.deliveryaddresssubmission,name="deliveryaddresssubmission"),
    path('checkout/paymentsection',views.paymentsection,name="paymentsection"),
    path('checkout/promocodevalidate',views.promocodevalidate,name="promocodevalidate"),
    path('checkout/pay',views.pay,name="pay"),
    path('order',views.order,name="order")

]
