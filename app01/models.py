from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



# min = 10000000000
# max = 99999999999

class Owner(models.Model):
    # id = models.IntegerField(
    #     validators = [
    #         MinValueValidator(min),
    #         MaxValueValidator(max)
    #     ],
    #     primary_key = True
    # )
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    address = models.TextField(max_length=200)

class House(models.Model):
    # id = models.IntegerField(
    #     validators = [
    #         MinValueValidator(min),
    #         MaxValueValidator(max),
    #     ],
    #     primary_key = True
    # )
    owners = models.ForeignKey(Owner,on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    maxnum = models.IntegerField(
        validators = [
            MinValueValidator(1),
            MaxValueValidator(10)
        ])
    charge = models.FloatField()
    state = models.BooleanField()

class Tenant(models.Model):
    # id = models.IntegerField(
    #     validators = [
    #         MinValueValidator(min),
    #         MaxValueValidator(max),
    #     ],
    #     primary_key = True
    # )
    name = models.CharField(max_length=10)
    birth = models.DateTimeField()
    sex = models.BooleanField()
    phone = models.CharField(max_length=11)
    address = models.ForeignKey(House,on_delete=models.CASCADE)

