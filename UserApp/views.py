from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .forms import CustomerSignupForm
from django.contrib.auth.forms import AuthenticationForm
from AdminApp.models import User,Slider_Image
from HotelmgmtApp.models import Add_room,Room_cat
from .models import Reservation,Feedback
from .forms import Reservation_Form
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test


def is_User(user):
    return user.is_authenticated and user.isUser and user.is_active

# User Index Page

def index_page(request):
    slider = Slider_Image.objects.filter(slider_status='enable')
    feedback = Feedback.objects.filter(feedback_status='True')
    rc= Room_cat.objects.all()
    room = Add_room.objects.all().order_by('-id')[:3]
    feedback_total = Feedback.objects.filter(feedback_status='True').count()
    room_total = Add_room.objects.all().count()
    reserve_total = Reservation.objects.filter(res_status__in=['Enabled','Disabled']).count()
    return render(request,'index.html',{'slider':slider, 'rc':rc,'feedback':feedback, 'room':room,'feedback_total':feedback_total,'room_total':room_total,'reserve_total':reserve_total })

def About_page(request):
    slider = Slider_Image.objects.filter(slider_status='enable')
    feedback = Feedback.objects.filter(feedback_status='True')
    return render(request,'about.html',{'slider':slider ,'feedback':feedback})



# User Registeration Page
class Customer_register(CreateView):
    model = User
    form_class = CustomerSignupForm
    template_name = 'registeraion-page.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return  redirect ('customer_login')
    
    
# User Login Page
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            request.session['user_name'] = username
            request.session['password'] = password
            
            
            if  user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,"Invalid username And password")
        else:
            messages.error(request,"Invalid username And password")
    return render(request,'login-page.html', context={'form':AuthenticationForm()})

# Logout Page
@user_passes_test(is_User, login_url='/customer_login/')
def logout_page(request):
    logout(request)
    return redirect('customer_login')

# Profile View And Edit Pages
@user_passes_test(is_User, login_url='/customer_login/')
def Profile_page(request):
    uname = request.user.username
    user=User.objects.get(username=uname)
    return render(request,'user_profile.html',{'user':user}) 

@user_passes_test(is_User, login_url='/customer_login/')
def ProfileEdit_page(request,name):
    user=User.objects.get(username=name)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        name = request.POST.get('name')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        return redirect('u_profile')        
    return render(request,'user_profile_edit.html',{'user':user}) 


# Gallery Page
def Room_display(request):
    # reserve = Reservation.objects.values_list('id', flat=True)
    # room = Add_room.objects.exclude(id__in=reserve)
    room = Add_room.objects.all()
    slider = Slider_Image.objects.filter(slider_status='enable')
    return render(request,'rooms.html',{'room': room,'slider':slider})


# Room Reservation Page
@user_passes_test(is_User, login_url='/customer_login/')
def Reservation_page(request, id):
    room = Add_room.objects.get(id=id)
    form = Reservation_Form()
    if request.method == "POST":
        form = Reservation_Form(request.POST)
        if form.is_valid():
            check_in_date =form.cleaned_data.get('check_in_date')
            check_out_date =form.cleaned_data.get('check_out_date')
            res_status = form.cleaned_data.get('res_status')
            r_id = form.cleaned_data.get('r_id')
            username = form.cleaned_data.get('username')
            
            existing_reservations = Reservation.objects.filter(r_id=r_id,check_in_date__lte=check_in_date, check_out_date__gte=check_in_date,res_status__in=['Disabled', 'Booked'])
            
            if existing_reservations.exists():
                error_message = "This room is already booked for the selected dates."
                return render(request, 'reservation_form.html', {'room': room, 'form': form, 'error_message': error_message})

            
            reserve = Reservation(username=username,r_id=r_id,check_in_date=check_in_date,check_out_date=check_out_date,res_status=res_status)
            reserve.save()
            r_id = request.POST.get('r_id')
            # form.save()
            return render (request,'feedback_model.html',{'r_id':r_id})
        else:
            print(form.errors)
    return render(request, 'reservation_form.html', {'room': room,'form': form, })





# Search Room Page
def check_availability(request):
    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        r_cat = request.POST.get('r_cat')
        r_capacity = request.POST.get('r_capacity')
        
        # Filter reservations that conflict with the requested dates
        conflicting_reservations = Reservation.objects.filter(
            check_in_date__lte=check_in_date, check_out_date__gte=check_in_date
        )

        # Exclude rooms booked during the requested dates
        booked_room_ids = conflicting_reservations.values_list('r_id', flat=True)
        available_rooms = Add_room.objects.exclude(id__in=booked_room_ids)

        # Filter available rooms based on category and capacity
        room = available_rooms.filter(
            r_cat=r_cat,
            r_capacity=r_capacity
        )

        # Pass the available rooms to the template for rendering
        return render(request, 'rooms.html', {'room': room})
        # context_data = {'room':room}

    return redirect('home')





# User Booking Detail
@user_passes_test(is_User, login_url='/customer_login/')
def Customer_Book_Detail(request):
    uname = request.user.username
    detail = Reservation.objects.filter(username=uname, res_status='Booked').order_by('-id')
    
    return render(request,'Book_detail.html',{'detail':detail})
    
    
# User Cancel Booking 
@user_passes_test(is_User, login_url='/customer_login/')
def Customer_reservation_cancel(request,id):
    reserve = Reservation.objects.get(id=id)
    reserve.res_status = 'Cancelled'
    
    user_obj = User.objects.get(username=reserve.username)  # Replace 4 with the actual user ID

    # Convert the User object to a string (e.g., using the username)
    username_str = str(user_obj.username)
    
    check_in_date = str(reserve.check_in_date)
    current_date = timezone.now().date()
    
    subject = 'Booking Cancel'
    message_lines = [
    username_str,
    'Cancell their reservation of'+' ' +check_in_date +' '+ 'cancell date' + str(current_date),
    ]
    message = '\n'.join(message_lines)
    from_email = 'eproject.apt@gmail.com'  # Replace with your Gmail email address
    recipient_list = ['eproject.apt@gmail.com']  # Replace with the recipient's email address

    send_mail(subject, message, from_email, recipient_list)
        
    reserve.save()
    return redirect('home') 
    # return render(request,'Book_detail.html',{'detail':detail}) 
    
    
def singl_room(request,id):
    room = Add_room.objects.get(id=id)
    slider = Slider_Image.objects.filter(slider_status='enable')
    count_5star = Feedback.objects.filter(rating='5star',r_id=room.id).count()
    count_4star = Feedback.objects.filter(rating='4star',r_id=room.id).count()
    count_3star = Feedback.objects.filter(rating='3star',r_id=room.id).count()
    count_2star = Feedback.objects.filter(rating='2star',r_id=room.id).count()
    count_1star = Feedback.objects.filter(rating='1star',r_id=room.id).count()
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            message = request.POST.get('message')
            rating = request.POST.get('option')
            r_id = room.id
            uname = request.user.username
            
            r_id = Add_room.objects.get(id=r_id)
            username=User.objects.get(username=uname)
            
            feedback = Feedback(username=username,r_id=r_id,message=message,rating=rating)
            feedback.save()
            return redirect('room') 
        return redirect('customer_login')
    return render (request,'Room-single.html',{'room':room,  'slider':slider,'count_5star': count_5star,
        'count_4star': count_4star,
        'count_3star': count_3star,
        'count_2star': count_2star,
        'count_1star': count_1star,})






@user_passes_test(is_User, login_url='/customer_login/')
def Feedback_page(request):  
    if request.method == 'POST':
    
        message = request.POST.get('message')
        rating = request.POST.get('option')
        r_id = request.POST.get('r_id')
        uname = request.user.username
        
        r_id = Add_room.objects.get(id=r_id)
        username=User.objects.get(username=uname)
        
        feedback = Feedback(username=username,r_id=r_id,message=message,rating=rating)
        feedback.save()
        return redirect('home')
    return render (request,'feedback_model.html')