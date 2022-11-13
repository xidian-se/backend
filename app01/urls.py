from django.urls import path
from app01 import views


app_name = 'app01'

urlpatterns = [
    # path('',views.onwer_list,name='list')  
    # path('owner',views.own_reg)
    # path('tenant',views.ten_reg)
    path('login',views.login,name='login'),
]
