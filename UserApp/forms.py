from AdminApp.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Reservation,Feedback
from HotelmgmtApp.models import Add_room


class  CustomerSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(required=True)
    
    
    class Meta(UserCreationForm.Meta):
        model = User
        
    def save(self):
        user = super().save(commit=False)
        user.isUser = True
        user.is_active = False
        user.email = self.cleaned_data.get('email')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.first_name = self.cleaned_data.get('first_name')
        user.save()
        return user
    
    
# class Reservation_Form(forms.Form):
#     username = forms.CharField()
#     r_id =  forms.IntegerField()
#     res_status = forms.CharField()
#     check_in_date = forms.DateField()
#     check_out_date = forms.DateField()

class Reservation_Form(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['username','r_id','res_status','check_in_date','check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY'}),
        }
        input_formats = ['%d-%m-%Y']  # Specify the input format

class Feedback_form(forms.Form):
    message =forms.CharField()
    rating =forms.CharField()
    