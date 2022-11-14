from django.shortcuts import render

# Create your views here.
from .models import *
# from app01.serializer import OwnerListSerializer
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

# @api_view(['GET','POST'])
# def onwer_list(request):
#     if request.method == 'GET':
#         owners = Owner.objects.all()
#         serializer = OwnerListSerializer(owners,many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = OwnerListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Deal with the login issue.
def login(request):
    if request.method == "POST":
        username_to_get = request.POST.get("username")
        password_to_eval = request.POST.get("password")
        try:
            temp = Account.objects.get(username=username_to_get)
        except Account.DoesNotExist:
            return JsonResponse({"isLogin": False, "reason":"用户没找到"})
        else:
            if temp.password == password_to_eval:
                request.session["id"] = temp.id
                request.session["identity"] = temp.identity
                identity =
                return JsonResponse({"isLogin": True, "reason":"你咋这么多废话"})
            else:
                return JsonResponse({"isLogin": False, "reason":"密码错误"})
    else:
        return JsonResponse({"isLogin": False, "reason":"没有使用 POST"})

#  TO DO
def reg_ten(request):
    res=json.encoder.JSONEncoder().encode({'ok':True})
    print(res)
    return JsonResponse(res,safe=False)

#  TO DO
def reg_own(request):
    res=json.encoder.JSONEncoder().encode({'ok':True})
    print(res)
    return JsonResponse(res,safe=False)
    
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
