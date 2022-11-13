from django.contrib import admin
from .models import Owner,Tenant,House
# Register your models here.
admin.site.register(Owner)
admin.site.register(Tenant)
admin.site.register(House)