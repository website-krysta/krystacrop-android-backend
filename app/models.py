from django.db import models
from django.utils import timezone
# Create your models here.
class user(models.Model):
    UserID = models.AutoField(primary_key=True)
    EmailID = models.EmailField(unique=True)
    Password = models.CharField(max_length=25, blank=False)
    Role = models.CharField(max_length=15, blank=True)
    UserStatus = models.BooleanField(default=True)
  
    def __str__(self):
            return self.EmailID

class orders(models.Model):
    OrdersId = models.AutoField(primary_key=True)
    DealerName = models.CharField(max_length=60)
    TransporterName = models.CharField(max_length=560)
    Address = models.CharField(max_length=100)
    ProductName = models.CharField(max_length=60)
    ProductQuantity = models.IntegerField()
    DateStr = models.CharField(max_length=12)
    TimeStr = models.CharField(max_length=12)
    AddedTime = models.DateTimeField(default=timezone.now)
    UpdatedTime = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
            return self.DealerName
