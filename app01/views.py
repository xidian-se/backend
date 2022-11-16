from django.shortcuts import render

# Create your views here.
from .models import *
# from app01.serializer import OwnerListSerializer
from django.http import JsonResponse
import json

def only_get_data(identity, index):
    if identity == False:  # Tenant
        temp = Account.objects.get(id=index).tenant
        return {
            "name": temp.name,
            "birth": temp.birth,
            "sex": temp.sex,
            "phone": temp.phone,
            "address": temp.address,
        }
    elif identity == True:  # Owner
        temp = Account.objects.get(id=index).owner
        return {
            "name": temp.name,
            "phone": temp.phone,
            "address": temp.address,
        }
    else:
        return {"Error": "Not found"}

# Deal with the login issue.
# Get: {"username":xxx,"password":xxx}
# Return see the code. Session not tested.
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if request.session.get("isLogin") == True:
            return JsonResponse({
                "isLogin": True,
                "reason": "已经登录",
                "identity": request.session["identity"],
                "data": only_get_data(
                    request.session["identity"],
                    request.session["id"],
                )
            })
        try:
            temp = Account.objects.get(username=data.get("username"))
        except Account.DoesNotExist:
            return JsonResponse({"isLogin": False, "reason": "用户没找到"})
        else:
            if temp.password == data.get("password"):
                data = {}
                if temp.identity == False:  # Tenant
                    data = {
                        "identity": False,
                        "reason": "租客登录",
                        "data": {
                            "name": temp.tenant.name,
                            "birth": temp.tenant.birth,
                            "sex": temp.tenant.sex,
                            "phone": temp.tenant.phone,
                            "address": temp.tenant.address,
                        },
                    }
                elif temp.identity == True:  # Owner
                    data = {
                        "identity": True,
                        "reason": "房主登录",
                        "data": {
                            "name": temp.owner.name,
                            "phone": temp.owner.phone,
                            "address": temp.owner.address,
                        },
                    }
                else:
                    return JsonResponse({"isLogin": False, "reason": "在判断用户信息时候出错"})
                request.session["id"] = temp.id
                request.session["identity"] = temp.identity
                request.session["isLogin"] = True
                data["isLogin"] = True
                return JsonResponse(data)
            else:
                return JsonResponse({"isLogin": False, "reason": "密码错误"})
    elif request.method == "GET":
        if request.session.get("isLogin") == True:
            return JsonResponse({
                "isLogin": True,
                "reason": "已经登录",
                "identity": request.session["identity"],
                "data": only_get_data(
                    request.session["identity"],
                    request.session["id"],
                )
            })
        else:
            return JsonResponse({"isLogin": False, "reason": "没有登录"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "POST 登录 GET 检测状态"})

# Deal with the logout issue. Just clear the session.
# Return see the code. Session not tested.
def logout(request):
    if request.method == "POST":
        request.session.clear()
        return JsonResponse({"isSuccess": True, "reason": "登录状态被清除"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "POST 登录 GET 检测状态"})


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
            return JsonResponse({"isSuccess": False, "reason": "用户名重复"})
        # Make sure it's a full crab. I'm pretty sure it is a rare condition.
        if ('name' not in data.keys()):
            return JsonResponse({"isSuccess": False, "reason": "发送名字有空的"})
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
        return JsonResponse({"isSuccess": True, "reason": "创建成功"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "没有使用 POST"})


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
            return JsonResponse({"isSuccess": False, "reason": "用户名重复"})
        # Make sure it's a full crab. I'm pretty sure it is a rare condition.
        if ('name' not in data.keys()):
            return JsonResponse({"isSuccess": False, "reason": "发送名字有空的"})
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
        return JsonResponse({"isSuccess": True, "reason": "创建成功"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "没有使用 POST"})

# Update tenant information
# Get: {
#   "name": "",
#   "address": "",
#   "sex": "",
#   "phone": "",
#   "birth": "",
#   "username": "",
#   "password": ""
# }
# Return see the code.
def ten_up(request):
    if request.method == "POST":
        # See if has the same name here.
        data = json.loads(request.body)
        try:
            to_change = Account.objects.get(username=data.get("username"))
        except Account.DoesNotExist:
            return JsonResponse({"isSuccess": False, "reason": "用户没找到"})
        else:
            # Identity check.
            if request.session["id"] == to_change.id:
                return JsonResponse({"isSuccess": False, "reason": "非本人操作"})
            # Make sure it's a full crab. I'm pretty sure it is a rare condition.
            if ('name' not in data.keys()):
                return JsonResponse({"isSuccess": False, "reason": "发送名字有空的"})
            # Change data
            to_change["username"] = data["username"],
            to_change["password"] = data["password"],
            to_change["name"] = data["name"],
            to_change["address"] = data["address"],
            to_change["sex"] = data["sex"],
            to_change["phone"] = data["phone"],
            to_change["birth"] = data["birth"],
            return JsonResponse({"isSuccess": True, "reason": "修改成功"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "没有使用 POST"})


# Update owner information
# {
#   "name": "",
#   "address": "",
#   "phone": "",
#   "username": "",
#   "password": ""
# }
#Return see the code.
def own_up(request):
    if request.method == "POST":
        # See if has the same name here.
        data = json.loads(request.body)
        try:
            to_change = Account.objects.get(username=data.get("username"))
        except Account.DoesNotExist:
            return JsonResponse({"isSuccess": False, "reason": "用户没找到"})
        else:
            # Identity check.
            if request.session["id"] == to_change.id:
                return JsonResponse({"isSuccess": False, "reason": "非本人操作"})
            # Make sure it's a full crab. I'm pretty sure it is a rare condition.
            if ('name' not in data.keys()):
                return JsonResponse({"isSuccess": False, "reason": "发送名字有空的"})
            # Change data
            to_change["username"] = data["username"],
            to_change["password"] = data["password"],
            to_change["name"] = data["name"],
            to_change["address"] = data["address"],
            to_change["phone"] = data["phone"],
            return JsonResponse({"isSuccess": True, "reason": "修改成功"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "没有使用 POST"})

# GET tenant info
def ten_info(request):
    if request.session["identity"] == False:
        return JsonResponse(only_get_data(request.session["identity"],request.session["id"]))
    else:
        return JsonResponse({"isSuccess": False, "reason": "不是请求租户或者没有登录"})

# GET owner info
def own_info(request):
    if request.session["identity"] == True:
        return JsonResponse(only_get_data(request.session["identity"],request.session["id"]))
    else:
        return JsonResponse({"isSuccess": False, "reason": "不是请求房主或者没有登录"})

# API for house. My sweet home.
# The folling data sent to me is used to add the house information.
# {
#   "name": "",
#   "address": "",
#   "total": 0,
#   "rent": 0,
#   "price": 0,
#   "description": ""
# }
# The folling data sent to me is used to update the house information.
# {
#   "id": "",
#   "name": "",
#   "address": "",
#   "total": 0,
#   "rent": 0,
#   "price": 0,
#   "description": ""
# }
# Return see the code. (这句话是中式英语)
# NOT TESTED!
def houseinfo(request):
    if request.method == "POST":
        # Check is owner login.
        if request.session["identity"] != True:
            return JsonResponse({"isSuccess": False, "reason": "不是房主身份登录"})
        # Start dealing.
        data = json.loads(request.body)
        temp = Account.objects.get(id=request.session["id"]).owner
        if "id" in data: # Update
            # Check if it is the owner.
            to_change = House.objects.get(id=data["id"])
            if to_change.owners != temp.owner:
                return JsonResponse({"isSuccess": False, "reason": "不是房主本人登录"})
            # Start updating.
            to_change.name = data["name"]
            to_change.address = data["address"]
            to_change.maxnum = data["total"]
            to_change.rent = data["rent"]
            to_change.price = data["price"]
            to_change.description = data["description"]
            return JsonResponse({"isSuccess": True, "reason": "修改成功"})
        else: # Add
            House.object.create(
                owner = temp,
                name = data["name"],
                address = data["address"],
                maxnum = data["total"],
                rent = data["rent"],
                price = data["price"],
                description = data["description"],
            )
            return JsonResponse({"isSuccess": True, "reason": "添加成功"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "没有使用 POST"})