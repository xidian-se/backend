from django.urls import path
from app01 import views


app_name = 'app01'
urlpatterns = [
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('pay',views.pay, name='pay'),
    path('register/tenant', views.reg_ten, name='reg_ten'),
    path('register/owner',views.reg_own, name='reg_own'),
    path('tenant/update',views.ten_up,name='up_ten'),    
    path('tenant/info',views.ten_info,name='ten_info'),
    path('tenant/request',views.ten_req,name='ten_req'),
    path('tenant/payinfo',views.ten_payinfo,name='ten_payinfo'),
    path('owner/info',views.own_info,name='own_info'),
    path('owner/update',views.own_up,name='up_own'),
    path('owner/houseinfo',views.houseinfo,name='houseinfo'),
    path('owner/housedels',views.housedels,name='housedels'),
    path('owner/cancel',views.own_cancel,name='own_cancel'),
    path('owner/confirm',views.own_confirm,name='own_confirm'),
    path('owner/opinfo',views.own_opinfo,name='own_opinfo'),
    path('owner/statistics',views.own_statistics,name='own_statistics'),
    path('owner/payinfo',views.own_payinfo,name='own_payinfo'),
]
