from django.shortcuts import render

# Create your views here.
from .models import Owner
from app01.serializer import OwnerListSerializer
from django.http import JsonResponse

def onwer_list(request):
    owners = Owner.objects.all()
    serializer = OwnerListSerializer(owners, many=True)
    return JsonResponse(serializer.data, safe=False)
