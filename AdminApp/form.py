from .models import Employee, User, Slider_Image
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms

class  EmployeeSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(required=True)
    designation = forms.CharField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.isAdmin = True
        user.is_staff = True
        user.email = self.cleaned_data.get('email')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.first_name = self.cleaned_data.get('first_name')
        user.save()
        employee =  Employee.objects.create(user=user)
        employee.designation = self.cleaned_data.get('designation')
        employee.save()
        return user
    
class Slider_Image_Form(forms.Form):
    image = forms.ImageField()
    slider_status = forms.CharField()