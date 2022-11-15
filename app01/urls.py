from django.urls import path
from app01 import views


app_name = 'app01'
urlpatterns = [
    # path('',views.onwer_list,name='list')  
    path('login',views.login, name='login'),
    path('register/tenant', views.reg_ten, name='reg_ten'),
    path('register/owner',views.reg_own, name='reg_own'),
    path('tenant/update',views.ten_up,name='up_ten'),
    path('owner/update',views.own_up,name='up_own'),
]
