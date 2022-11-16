from django.urls import path
from app01 import views


app_name = 'app01'
urlpatterns = [
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('register/tenant', views.reg_ten, name='reg_ten'),
    path('register/owner',views.reg_own, name='reg_own'),
    path('tenant/update',views.ten_up,name='up_ten'),
    path('owner/update',views.own_up,name='up_own'),
    path('tenant/info',views.ten_info,name='ten_info'),
    path('owner/info',views.own_info,name='own_info'),
    path('owner/houseinfo',views.houseinfo,name='houseinfo'),
    path('owner/housedels',views.housedels,name='housedels'),
]
