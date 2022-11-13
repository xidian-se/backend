from django.shortcuts import render

# Create your views here.
from .models import Owner
# from app01.serializer import OwnerListSerializer
from django.http import JsonResponse
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

#  TO DO
def login(request):
    res=json.encoder.JSONEncoder().encode({'ok':True})
    print(res)
    return JsonResponse(res,safe=False)

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