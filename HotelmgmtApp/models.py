from django.db import models
# Create your models here.


class Room_cat(models.Model):
    rc_name = models.CharField("RC_NAME", max_length=100)
    rc_des =  models.CharField("RC_description",max_length=225)
    # def get_features_list(self):
    #     return self.rc_des.split(', ')
    
class Add_room(models.Model):
    r_no = models.CharField("Room_Number",max_length=100)
    r_bed_no = models.CharField("Number_Of_Bed", max_length=100) 
    r_capacity = models.IntegerField("Room Capacity") 
    r_price = models.IntegerField("Price")
    r_cat = models.ForeignKey(Room_cat, on_delete=models.CASCADE)
    room_img = models.ImageField(upload_to='img', blank=True)
    
