from django.urls import URLPattern, path,re_path
from . import views
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.contrib.auth import views as auth_views
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
    re_path('^cart/(?P<productid>[a-zA-Z0-9!@#$&()\\-`_.+,/\"]*)',views.cart,name="cart"),
    path('cartmodifyquantity',views.cartmodifyquantity,name='cartmodifyquantity'),
    path('priceDetailsUpdateSection',views.priceDetailsUpdateSection,name='priceDetailsUpdateSection'),
    re_path('^wishlist/(?P<productid>[a-zA-Z0-9!@#$&()\\-`_.+,/\"]*)',views.wishlist,name="wishlist"),
    re_path('^checkout/deliveryaddress/(?P<productid>[a-zA-Z0-9!@#$&()\\-`_.+,/\"]*)',views.checkoutdeliveryaddress,name="checkoutdeliveryaddress"),
    path('deliveryaddresssubmission',views.deliveryaddresssubmission,name="deliveryaddresssubmission"),
    re_path('^checkout/paymentsection/(?P<productid>[a-zA-Z0-9!@#$&()\\-`_.+,/\"]*)',views.paymentsection,name="paymentsection"),
    path('checkout/promocodevalidate',views.promocodevalidate,name="promocodevalidate"),
    re_path('^checkout/pay/(?P<productid>[a-zA-Z0-9!@#$&()\\-`_.+,/\"]*)',views.pay,name="pay"),
    path('order',views.order,name="order"),
    path('cartorderremove',views.cartorderremove,name="cartorderremove"),
    path('productCommentSubmission',views.productCommentSubmission,name="productCommentSubmission"),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='shop/resetpassword.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='shop/resetpasswordsent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='shop/passwordresetform.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='shop/resetpassworddone.html'),name='password_reset_complete'),
    path('profile',views.profile,name='profile'),
    path('profileupdate',views.profileupdate,name='profileupdate')


]
