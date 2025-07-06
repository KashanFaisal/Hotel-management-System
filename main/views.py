from django.shortcuts import render ,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from AdminApp.models import User,Slider_Image



def Contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        
        subject = subject
        message_lines = [
        name,
        message,
        ]
        message = '\n'.join(message_lines)
        from_email = 'kashan.faisal2001@gmail.com'  # Replace with your Gmail email address
        recipient_list = [email]  # Replace with the recipient's email address

        send_mail(subject, message, from_email, recipient_list)

        
        return redirect('home')
    
    return render(request, 'contact.html')

