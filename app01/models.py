from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Owner(models.Model):
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=50)


class House(models.Model):
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    maxnum = models.IntegerField(
        validators = [
            MinValueValidator(1),
            MaxValueValidator(10)
        ])
    rent = models.IntegerField(validators = [
            MinValueValidator(0),
            MaxValueValidator(maxnum)
        ])
    price = models.FloatField()

class Tenant(models.Model):
    name = models.CharField(max_length=10)
    birth = models.DateTimeField()
    # 根据网络用语习惯，False 代表女生，True 代表男生
    sex = models.BooleanField()
    phone = models.CharField(max_length=11)
    # 联系地址和租住地址
    address = models.CharField(max_length=50)
    renting = models.ForeignKey(House,on_delete=models.CASCADE,blank=True,null=True)


# 当租客请求租房子时候，这里储存租客和房子的联系，成功/失败会撤回的
class Relation(models.Model):
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE)
    house = models.ForeignKey(House,on_delete=models.CASCADE)
    paid = models.BooleanField()

# 存储帐号信息，identity 真为 Owner 假为 Tenant
class Account(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    identity = models.BooleanField()
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE,blank=True,null=True)
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE,blank=True,null=True)
