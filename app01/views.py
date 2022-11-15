from django.shortcuts import render

# Create your views here.
from .models import *
# from app01.serializer import OwnerListSerializer
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

# Deal with the login issue.
# Get: {"username":xxx,"password":xxx}
# Return see the code. Session not tested.
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if request.session.get("isLogin") == True:
            return JsonResponse({"isLogin": True, "reason":"已经登录"})
        try:
            temp = Account.objects.get(username=data.get("username"))
        except Account.DoesNotExist:
            return JsonResponse({"isLogin": False, "reason":"用户没找到"})
        else:
            if temp.password == data.get("password"):
                data = {}
                if temp.identity == False: # Tenant
                    data = {
                        "identity": False,
                        "reason":"租客登录",
                        "data": {
                            "name": temp.tenant.name,
                            "birth": temp.tenant.birth,
                            "sex": temp.tenant.sex,
                            "phone": temp.tenant.phone,
                            "address": temp.tenant.address,
                        },
                    }
                elif temp.identity == True: # Owner
                    data = {
                        "identity": False,
                        "reason":"租客登录",
                        "data": {
                            "name": temp.owner.name,
                            "phone": temp.owner.phone,
                            "address": temp.owner.address,
                        },
                    }
                else:
                    return JsonResponse({"isLogin": False, "reason":"在判断用户信息时候出错"})
                request.session["id"] = temp.id
                request.session["identity"] = temp.identity
                data["isLogin"] = True
                return JsonResponse(data)
            else:
                return JsonResponse({"isLogin": False, "reason":"密码错误"})
    else:
        return JsonResponse({"isLogin": False, "reason":"没有使用 POST"})

# Add a tenant account.
# Get: {
#  "name": "",
#  "address": "",
#  "sex": "",
#  "phone": "",
#  "birth": "",
#  "username": "",
#  "password": ""
# }
# Return see the code.
def reg_ten(request):
    if request.method == "POST":
        # See if has the same name here.
        data = json.loads(request.body)
        if Account.objects.filter(username=data.get("username")).exists():
            return JsonResponse({"isSuccess": False, "reason":"用户名重复"})
        # Make sure it's a full crab. I'm pretty sure it is a rare condition.
        if ('name' not in data.keys()):
            return JsonResponse({"isSuccess": False, "reason":"发送名字有空的"})
        # Add new user.
        '''
        Tenant.objects.create(
            name=data["name"],
            address=data["address"],
            sex=data["sex"],
            phone=data["phone"],
            birth=data["birth"],
        )
        '''
        Account.objects.create(
            username=data["username"],
            password=data["password"],
            identity=False,
            tenant=Tenant.objects.get_or_create(
                name=data["name"],
                address=data["address"],
                sex=data["sex"],
                phone=data["phone"],
                birth=data["birth"],
            )[0]
        )
        return JsonResponse({"isSuccess": True, "reason":"创建成功"})
    else:
        return JsonResponse({"isSuccess": False, "reason":"没有使用 POST"})


# Add a owner account.
# Get: {
#  "name": "",
#  "address": "",
#  "phone": "",
#  "username": "",
#  "password": ""
# }
# Return see the code.
def reg_own(request):
    if request.method == "POST":
        # See if has the same name here.
        data = json.loads(request.body)
        if Account.objects.filter(username=data.get("username")).exists():
            return JsonResponse({"isSuccess": False, "reason":"用户名重复"})
        # Make sure it's a full crab. I'm pretty sure it is a rare condition.
        if ('name' not in data.keys()):
            return JsonResponse({"isSuccess": False, "reason":"发送名字有空的"})
        # Add new user.
        '''
        Owner.objects.create(
            name=data["name"],
            address=data["address"],
            phone=data["phone"],
        )
        '''
        Account.objects.create(
            username=data["username"],
            password=data["password"],
            identity=True,
            owner=Owner.objects.get_or_create(
                name=data["name"],
                address=data["address"],
                phone=data["phone"],
            )[0]
        )
        return JsonResponse({"isSuccess": True, "reason":"创建成功"})
    else:
        return JsonResponse({"isSuccess": False, "reason":"没有使用 POST"})
    
#  TO DO
def ten_up(request):
    res=json.encoder.JSONEncoder().encode({'ok':True})
    print(res)
    return JsonResponse(res,safe=False)

#  TO DO
def own_up(request):
    res=json.encoder.JSONEncoder().encode({'ok':True})
    print(res)
    return JsonResponse(res,safe=False)
