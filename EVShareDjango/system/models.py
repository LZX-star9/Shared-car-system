from django.db import models
from django.db.models.functions import Now
from django.contrib.auth.models import BaseUserManager,AbstractUser

# Create your models here.

class User(AbstractUser):
    USER_TYPES = [
        ("CS", "Customer"),
        ("OP", "Operator"),
        ("MN", "Manager"),
    ]
    username = models.CharField(max_length=20,null=False,unique=True)
    password = models.CharField(max_length=20,null=False)
    surname = models.CharField(max_length=20,null=False,default="")
    firstname = models.CharField(max_length=20,blank=True)
    telephone = models.CharField(max_length=20,blank=True)
    email = models.EmailField(null=True)
    registrationDate = models.DateTimeField(auto_now_add=True,null=True)
    userType = models.CharField(max_length=2,null=False,default="CS",choices=USER_TYPES)
    isActive = models.BooleanField(default=True)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    balance = models.FloatField(null=False,default=0)
    cardType = models.IntegerField(null=False,default=0)
    cardExpiry = models.DateField(null=False,default='2024-01-01')

class Location(models.Model):
    locationName = models.CharField(max_length=50,null=False)
    locationAddress = models.CharField(max_length=100,null=False)
    locationLat = models.FloatField(null=False)
    locationLong = models.FloatField(null=False)
    isAvailable = models.BooleanField(default=True)

class Vehicle(models.Model):
    vehicleType = models.CharField(max_length=10,null=False,default="EBike")
    vehicleLat = models.FloatField(null=True)
    vehicleLong = models.FloatField(null=True)
    charge = models.IntegerField(null=False,default=100)
    needsRepair = models.BooleanField(default = False)
    isParked = models.BooleanField(default = True)
    lastLocation = models.ForeignKey('system.Location', on_delete=models.RESTRICT)

class RentLog(models.Model):
    customer = models.ForeignKey('system.User', on_delete=models.RESTRICT)
    vehicle = models.ForeignKey('system.Vehicle', on_delete=models.RESTRICT)
    price = models.FloatField(null=False,default=0)
    startDate = models.DateTimeField(auto_now_add=True,null=True)
    endDate = models.DateTimeField(null=True)
    returnLocation = models.ForeignKey('system.Location', on_delete=models.RESTRICT,null=True)

class RepairLog(models.Model):
    MALFUNCTION_TYPE = [
        ("ER1", "Motor"),
        ("ER2", "Battery"),
        ("ER3", "Electronics"),
        ("ER4", "Cosmetic"),
        ("ER5", "Brakes"),
        ("ER6", "Direction"),
        ("ER7", "Other"),
    ]
    malfunctionType = models.CharField(max_length=15,null=False,default="Other",choices=MALFUNCTION_TYPE)
    reportDate = models.DateTimeField(auto_now_add=True,null=True)
    customer = models.ForeignKey('system.User', on_delete=models.RESTRICT, null=False,related_name="customer")
    vehicle = models.ForeignKey('system.Vehicle', on_delete=models.RESTRICT,null=False)
    description = models.CharField(max_length=100,null=False)
    operator = models.ForeignKey('system.User', on_delete=models.RESTRICT,null=True,related_name="operator")
    fixed = models.BooleanField(default=False)
    repairDate = models.DateTimeField(null=True)

class Payment(models.Model):
    customer = models.ForeignKey('system.User', on_delete=models.RESTRICT)
    remark = models.CharField(max_length=100,null=True)
    amount = models.IntegerField(null=False)
    paymentDate = models.DateTimeField(auto_now_add=True,null=True)