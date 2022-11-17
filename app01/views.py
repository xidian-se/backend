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
# Return see the code. 
def logout(request):
    request.session.clear()
    return JsonResponse({"isSuccess": True, "reason": "登录状态被清除"})

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
        if request.session["identity"] != False:
            return JsonResponse({"isSuccess": False, "reason": "不是租户身份登录"})
        # See if has the same name here.
        data = json.loads(request.body)
        try:
            to_change = Account.objects.get(id=request.session["id"]).tenant
            print(to_change.id)
        except Account.DoesNotExist:
            return JsonResponse({"isSuccess": False, "reason": "用户没找到"})
        else:
            # Make sure it's a full crab. I'm pretty sure it is a rare condition.
            if 'name' not in data.keys():
                return JsonResponse({"isSuccess": False, "reason": "发送名字有空的"})
            # Change data
            to_change.name = data["name"]
            to_change.address = data["address"]
            to_change.sex = data["sex"]
            to_change.phone = data["phone"]
            to_change.birth = data["birth"]
            to_change.save()
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
        if request.session["identity"] != True:
            return JsonResponse({"isSuccess": False, "reason": "不是房主身份登录"})
        # See if has the same name here.
        data = json.loads(request.body)
        try:
            to_change = Account.objects.get(id=request.session["id"]).owner
        except Account.DoesNotExist:
            return JsonResponse({"isSuccess": False, "reason": "用户没找到"})
        else:
            # Make sure it's a full crab. I'm pretty sure it is a rare condition.
            if ('name' not in data.keys()):
                return JsonResponse({"isSuccess": False, "reason": "发送名字有空的"})
            # Change data
            to_change.name = data["name"]
            to_change.address = data["address"]
            to_change.phone = data["phone"]
            to_change.save()
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
# POST:
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
# GET:
# With id, I can send you the detail of the house with the id.
# Else, I will show the information of the houses owned by this owner.
# Return see the code. (这句话是中式英语)
def houseinfo(request):
    # Check is owner login.
    if request.session["identity"] != True:
        return JsonResponse({"isSuccess": False, "reason": "不是房主身份登录"})
    # Start dealing.
    temp = Account.objects.get(id=request.session["id"]).owner
    if request.method == "POST":
        # Change the data.
        data = json.loads(request.body)
        if "id" in data: # Update
            # Check if it is the owner.
            to_change = House.objects.get(id=data["id"])
            if to_change.owner != temp:
                return JsonResponse({"isSuccess": False, "reason": "不是房主本人登录"})
            # Start updating. Need polish since not refrence.
            if "name" in data:
                print(to_change.name)
                print(data["name"])
                to_change.name = data["name"]
                print(to_change.name)
            if "address" in data:
                to_change.address = data["address"]
            if "total" in data:
                to_change.maxnum = data["total"]
            if "rent" in data:
                to_change.rent = data["rent"]
            if "price" in data:
                to_change.price = data["price"]
            if "description" in data:
                to_change.description = data["description"]
            to_change.save()
            return JsonResponse({"isSuccess": True, "reason": "修改成功"})
        else: # Add
            new = House(
                owner = temp,
                name = data["name"],
                address = data["address"],
                maxnum = data["total"],
                rent = data["rent"],
                price = data["price"],
                description = data["description"],
            )
            new.save()
            return JsonResponse({"isSuccess": True, "reason": "添加成功", "id": new.id})
    elif request.method == "GET":
        if type(request.body) == str: # Specific 
            house = House.objects.get(id=request.body["id"])
            if house.owner != temp:
                return JsonResponse({"isSuccess": False, "reason": "不是你的房子"})
            else:
                return JsonResponse({
                    "name": house.name,
                    "address": house.address,
                    "total": house.maxnum,
                    "rent": house.rent,
                    "price": house.price,
                    "description": house.description
                })
        else: # All house owned by this owner.
            results = House.objects.filter(owner=temp)
            to_return = []
            for i in results:
                to_return.append({
                    "id": i.id,
                    "name": i.name,
                    "address": i.address,
                    "total": i.maxnum,
                    "rent": i.rent,
                    "price": i.price,
                    "description": i.description
                })
            return JsonResponse(to_return,safe=False)
    else:
        return JsonResponse({"isSuccess": False, "reason": "POST添加修改GET获取信息"})

# Remove the house.
# POST:
# The folling data sent to me is used to add the house information.
# {
#   "id": "",
# }
# For the things that returns to you, see the code.
def housedels(request):
    if request.method == "POST":
        data = json.loads(request.body)
        house = House.objects.get(id=data["id"])
        if house.owner != Account.objects.get(id=request.session["id"]).owner:
            return JsonResponse({"isSuccess": False, "reason": "不是你的房子"})
        try:
            house.delete()
        except:
            return JsonResponse({"isSuccess": False, "reason": "删除失败"})
        else:
            return JsonResponse({"isSuccess": True, "reason": "删除成功"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "没有使用 POST"})

# API for pay.
# POST:
# Send me the code of the relation.
# If you are Owner, house id, else, relation id.
# {"id":xxx}
def pay(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if request.session["identity"] == False:
            try:
                code = Account.objects.get(id=data["id"])
            except Account.DoesNotExist:
                return JsonResponse({"isSuccess": False, "reason": "该订单不存在"})
            else:
                if request.session["id"] != code.tenant.id:
                    return JsonResponse({"isSuccess": False, "reason": "订单与该租户无关"})
                if code.house.rent >= code.house.maxnum:
                    return JsonResponse({"isSuccess": False, "reason": "该房屋已经满员"})
                if code.ten_paid == True:
                    return JsonResponse({"isSuccess": True, "reason": "该租户中介费已经结清"})
                else:
                    code.ten_paid = True
                    code.save()
                    JsonResponse({"isSuccess": True, "reason": "该租户中介费结清"})
        elif request.session["identity"] == True:
            try:
                code = House.objects.get(id=data["id"])
            except House.DoesNotExist:
                return JsonResponse({"isSuccess": False, "reason": "该房屋不存在"})
            else:
                if request.session["id"] != code.owner.id:
                    return JsonResponse({"isSuccess": False, "reason": "房屋与该户主无关"})
                if code.can_be_shown == True:
                    return JsonResponse({"isSuccess": True, "reason": "该房屋入场费已经结清"})
                else:
                    code.can_be_shown = True
                    code.save()
                    JsonResponse({"isSuccess": True, "reason": "该房屋入场费结清"})
        else:
            return JsonResponse({"isSuccess": False, "reason": "没有登录"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "没有使用 POST"})

# Tenant require renting a house.
# POST:
# {
#   id: // id of the house.
# }
# Will return the relation's id.
def ten_req(request):
    if request.method == "POST":
        if request.session["identity"] != False:
            return JsonResponse({"isSuccess": False, "reason": "非租户身份登录"})
        try:
            tenant = Tenant.objects.get(id=request.session["id"])
        except Tenant.DoesNotExist:
            return JsonResponse({"isSuccess": False, "reason": "租户信息没找到"})
        else:
            data = json.loads(request.body)
            house_to_rent = House.objects.get(id=data["id"])
            if house_to_rent.rent >= house_to_rent.maxnum:
                return JsonResponse({"isSuccess": False, "reason": "该房屋已经满员"})
            if tenant.renting == house_to_rent:
                return JsonResponse({"isSuccess": False, "reason": "该用户已经租住于此"})
            r = Relation(50,house_to_rent,tenant)
            r.save()
            return JsonResponse({"isSuccess": True, "reason": "请求已经发送", "id": r.id})
    else:
        return JsonResponse({"isSuccess": False, "reason": "没有使用 POST"})

# Tenant require canceling renting a house.
# No need to write, owner get the right to do it.
# Now owner could do the thing. Owner cancel api.
# POST me the id of the relation.
def own_cancel(request):
    if request.method == "POST":
        if request.session["identity"] != True:
            return JsonResponse({"isSuccess": False, "reason": "非户主身份登录"})
        data = json.loads(request.body)
        try:
            deal = Relation.objects.get(id=data["id"])
        except:
            return JsonResponse({"isSuccess": False, "reason": "没有查到订单"})
        else:
            if deal.house.owner != request.session["id"]:
                return JsonResponse({"isSuccess": False, "reason": "这房子不是你的"})
            if deal.tenant.renting != deal.house:
                return JsonResponse({"isSuccess": False, "reason": "他没有租住在这里"})
            if deal.ten_paid == False:
                return JsonResponse({"isSuccess": False, "reason": "租户没有清缴中介费"})
            deal.tenant.renting = None
            deal.house.rent -= 1
            deal.delete()
            return JsonResponse({"isSuccess": True, "reason": "退房成功"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "没有使用 POST"})

# Owner confirm the relation code api.
# POST
# ```json
#{
#  "id": "" ,// 租房操作id（其实就是租房对应关系的id）
#  "state": true/false // 确认租房或者取消租房
#}
def own_confirm(request):
    if request.method == "POST":
        if request.session["identity"] != True:
            return JsonResponse({"isSuccess": False, "reason": "非户主身份登录"})
        data = json.loads(request.body)
        try:
            deal = Relation.objects.get(id=data["id"])
        except:
            return JsonResponse({"isSuccess": False, "reason": "没有查到订单"})
        else:
            if deal.house.owner != request.session["id"]:
                return JsonResponse({"isSuccess": False, "reason": "这房子不是你的"})
            if deal.house.rent >= deal.house.maxnum:
                return JsonResponse({"isSuccess": False, "reason": "房屋已经满员"})
            if deal.ten_paid == False:
                return JsonResponse({"isSuccess": False, "reason": "租户没有清缴中介费"})
            if deal.tenant.renting != None:
                return JsonResponse({"isSuccess": False, "reason": "该租户已经租了另一个房子了"})
            if data["state"] == True:
                deal.tenant.renting = deal.house
                deal.house.rent += 1
                deal.save()
                return JsonResponse({"isSuccess": True, "reason": "出租成功"})
            if data["state"] == False:
                deal.delete()
                return JsonResponse({"isSuccess": True, "reason": "取消成功"})
    else:
        return JsonResponse({"isSuccess": False, "reason": "没有使用 POST"})

# Owner info get apis.

# /owner/opinfo
# json 数组的第一个是未确定的租房信息，需要房主改变状态，
# 第二个是正在租的信息，可以进行退租操作,也是一个数组，外层为房屋，
# children 内为租客，每个房屋为外层数组的一个元素。
def own_opinfo(request):
    if request.session["identity"] != True:
        return JsonResponse({"isSuccess": False, "reason": "非户主身份登录"})
    user = Account.objects.get(id=request.session["id"])
    # To be decided
    undecided = []
    results = Relation.objects.all()
    for i in results:
        if i.house.owner.id == user.owner.id and i.tenant.renting != i.house:
            undecided.append({
                "id": i.id,
                "name": i.house.name,
                "tenant": i.tenant.name,
                "phone": i.tenant.phone
            })
    # Decided
    dealt = []
    house = House.objects.all()
    for i in house:
        if i.owner.id == user.owner.id:
            to_append = { "name": i.name, "children": [] }
            for j in results:
                if j.house == i and j.tenant.renting == i:
                    to_append["children"].append({
                        "id": j.id,
                        "tenant": j.tenant.name,
                        "phone": j.tenant.phone,
                    })
            dealt.append(to_append)
    # Return
    return JsonResponse((undecided,dealt),safe=False)

# /owner/statistics
def own_statistics(request):
    if request.session["identity"] != True:
        return JsonResponse({"isSuccess": False, "reason": "非户主身份登录"})
    user = Account.objects.get(id=request.session["id"])
    # Empty, Partly, Full
    static = [0,0,0]
    information = []
    # Find all house
    house = House.objects.all()
    for i in house:
        if i.owner.id == user.owner.id:
            information.append({
                "name": i.name,
                "total": i.maxnum,
                "rent": i.rent,
            })
            if i.maxnum == i.rent:
                static[2] += 1
            elif i.rent == 0:
                static[0] += 1
            else:
                static[1] += 1
    # Return
    return JsonResponse((static,information),safe=False)

# /owner/payinfo
def own_payinfo(request):
    if request.session["identity"] != True:
        return JsonResponse({"isSuccess": False, "reason": "非户主身份登录"})
    user = Account.objects.get(id=request.session["id"])
    house_to_pay = House.objects.filter(owner=user.owner, can_be_shown=False)
    to_return = []
    for i in house_to_pay:
        to_return.append({
            "id": i.id,
            "name": i.name,
            "price": 670,
        })
    return JsonResponse(to_return,safe=False)

# /tenant/statistics
def ten_statistics(request):
    if request.session["identity"] != False:
        return JsonResponse({"isSuccess": False, "reason": "非租户身份登录"})
    user = Account.objects.get(id=request.session["id"])
    # Find all relation
    totalstat = 0
    information = []
    relation = Relation.objects.filter(tenant=user.tenant)
    for i in relation:
        # No fee not seen
        if i.ten_paid == False and i.house_shown == False:
            stat = 0
        # Fee but not seen
        elif i.ten_paid == True and i.house_shown == False:
            stat = 1
        # Fee, seen but decided
        elif i.ten_paid == True and i.house_shown == True:
            stat = 2
            # Fee, seen and rented
            if i.tenant.renting == i.house:
                stat = 3
        # Update total situation.
        if stat > totalstat:
            totalstat = stat
        # Append 
        information.append({
            "stat": stat,
            "name": i.house.name,
            "price": i.house.price,
            "owner": i.house.owner.name,
            "phone": i.house.owner.phone,
        })
    # Return
    return JsonResponse({"stat":totalstat,"detail":information},safe=False)

# /tenant/payinfo
def ten_payinfo(request):
    if request.session["identity"] != False:
        return JsonResponse({"isSuccess": False, "reason": "非租户身份登录"})
    user = Account.objects.get(id=request.session["id"])
    relation = Relation.objects.filter(tenant=user.tenant, ten_paid=False)
    to_return = []
    for i in relation:
        to_return.append({
            "id": i.id,
            "name": i.house.name,
            "price": 50,
        })
    return JsonResponse(to_return,safe=False)