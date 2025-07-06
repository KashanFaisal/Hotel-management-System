from django.db import models
from django.contrib.auth.models import AbstractUser
from HotelmgmtApp.models import Add_room
from datetime import datetime
# Create your models here.

class User(AbstractUser):
    isUser = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=15)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    designation = models.CharField(max_length=100)
    
class Slider_Image(models.Model):
    image = models.ImageField(upload_to ='slider_img', blank=False)
    slider_status = models.CharField('Slider Status', max_length=50)
    

class Check_Out(models.Model):
    username = models.ForeignKey(User,  on_delete=models.CASCADE, to_field='username')
    r_id = models.ForeignKey(Add_room, on_delete=models.CASCADE)
    check_in_date = models.DateField(blank=False)
    check_out_date = models.DateField(blank=False)
    
class Reservation_Reject(models.Model):
    username = models.ForeignKey(User,  on_delete=models.CASCADE, to_field='username')
    r_id = models.ForeignKey(Add_room, on_delete=models.CASCADE)
    check_in_date = models.DateField(blank=False)
    check_out_date = models.DateField(blank=False)
    res_reason = models.CharField(max_length=256)
    created_at = models.DateTimeField(default=datetime.now)    
    

    
    
