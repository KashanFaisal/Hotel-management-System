from django.db import models
from HotelmgmtApp.models import Add_room
from AdminApp.models import User

class Reservation(models.Model):
    username = models.ForeignKey(User,  on_delete=models.CASCADE, to_field='username')
    r_id = models.ForeignKey(Add_room, on_delete=models.CASCADE)
    check_in_date = models.DateField(blank=False)
    check_out_date = models.DateField(blank=False)
    res_status = models.CharField("Reservation Status", max_length=50)
    
    
class Feedback(models.Model):
    username = models.ForeignKey(User,  on_delete=models.CASCADE, to_field='username')
    r_id = models.ForeignKey(Add_room, on_delete=models.CASCADE)
    message =models.CharField(max_length=256,blank=False)
    rating =models.CharField(max_length=256,blank=False)
    feedback_status = models.CharField("Feedback Status", max_length=100,default=False)
    


    
 
