from django import forms
from .models import Room_cat,Add_room


class RoomcatForm(forms.Form):
    rc_name = forms.CharField()
    rc_des = forms.CharField()




class AddRoom_Form(forms.Form):
    r_no = forms.CharField()
    r_bed_no = forms.CharField()
    r_capacity = forms.IntegerField() 
    r_price = forms.IntegerField()
    r_cat = forms.IntegerField()
    room_img = forms.ImageField()
        
    