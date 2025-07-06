from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import EmployeeSignupForm, Slider_Image_Form
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Employee,Slider_Image,Check_Out,Reservation_Reject
from UserApp.models import Reservation,Feedback
from UserApp.forms import Reservation_Form
from HotelmgmtApp.models import Add_room
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime, timedelta




def is_admin(user):
    return user.is_authenticated and user.is_staff


# Dashboard Index Page
@user_passes_test(is_admin, login_url='/login/')
def dashboard(request):
    user = User.objects.filter(isUser= True, is_active=True).count()
    reserve = Reservation.objects.filter(res_status__in=['Disabled','Enabled']).count()
    room = Add_room.objects.all().count
    
    today = datetime.now().date()
    last_week_start = today - timedelta(days=today.weekday() + 7)
    last_week_end = last_week_start + timedelta(days=6)
    
    last_week_reservations = Reservation.objects.filter(check_in_date__range=[last_week_start, last_week_end])
    
    if last_week_reservations is not None:
        last_week_reservations = 0
    return render(request,'index-2.html',{'user':user,'reserve':reserve,'room':room,'last_week_reservations':last_week_reservations})

# Employee Registeration Page
class Employee_register(CreateView):
    model = User
    form_class = EmployeeSignupForm
    template_name = 'page-register.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return  redirect ('login')
    
# Employee Registeration Page end
    
# Employee Login Page
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
                if user.is_staff:
                    login(request, user)
                    return redirect('dashboard')
            else:
                messages.error(request,"Invalid username And password")
        else:
            messages.error(request,"Invalid username And password")
    return render(request,'page-login.html', context={'form':AuthenticationForm()})

# Employee Login Page end

# Employee Logout Page 
@user_passes_test(is_admin, login_url='/login/')
def logout_employee_page(request):
    logout(request)
    return redirect('login')

# Employe Logout page end



# Customer View, Customer Account Approval pages
@user_passes_test(is_admin, login_url='/login/')
def Customer_view(request):
    user_data = {}
    
    user_data["dataset"] = User.objects.filter(is_active = False)
    return render(request,'user_view.html',user_data)


@user_passes_test(is_admin, login_url='/login/')    
def Approve(request,id):
    user = User.objects.get(id=id)
    user.is_active = True
    email=user.email
    user.save()
    subject = 'ACCOUNT ACTIVATE'
    message = ('Your Account Has Been Activated')
    from_email = 'eproject.apt@gmail.com'  # Replace with your Gmail email address
    recipient_list = [email]  # Replace with the recipient's email address

    send_mail(subject, message, from_email, recipient_list)
    return redirect('customer_view')  

@user_passes_test(is_admin, login_url='/login/')
def Customer_list_page(request):
    user_data = {}
    
    user_data["dataset"] = User.objects.filter(is_active = True,isUser=True)
    return render(request,'User_list.html',user_data)

# Customer View, Customer Account Approval pages end 


# Profile view and edit pages
@user_passes_test(is_admin, login_url='/login/')
def Profile_page(request):
    uname = request.user.username
    user=User.objects.get(username=uname)
    employee = Employee.objects.get(user=user)
    return render(request,'profile.html',{'user':user, 'employee':employee})

 
@user_passes_test(is_admin, login_url='/login/')
def ProfileEdit_page(request,name):
    user=User.objects.get(username=name)
    employee = Employee.objects.get(user=user)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        name = request.POST.get('name')
        user.phone_number = request.POST.get('phone_number')
        employee.designation = request.POST.get('designation')
        user.save()
        employee.save()
        return redirect('profile')
        
        
    return render(request,'profile_edit.html',{'user':user, 'employee':employee}) 

# Carousel Add, View and Permision pages
@user_passes_test(is_admin, login_url='/login/')
def SliderImage_Page(request):
    if request.method == 'POST':
        form = Slider_Image_Form(request.POST,request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            slider_status = form.cleaned_data.get('slider_status')
            
            slider = Slider_Image(image=image,slider_status=slider_status)
            slider.save()
            return redirect('sliderimage_view')
        
    return render(request,'Add_Slider.html')


@user_passes_test(is_admin, login_url='/login/')
def SliderImage_View_Page(request):
    slider = Slider_Image.objects.all().order_by('-id')
    return render(request,'slider_image_view.html',{'slider':slider})

@user_passes_test(is_admin, login_url='/login/')
def SliderImage_Enable(request,id):
    slider = Slider_Image.objects.get(id=id)
    if slider.slider_status == 'disable': 
        slider.slider_status = 'enable'
    elif slider.slider_status == 'enable': 
        slider.slider_status = 'disable'
    
    slider.save()
    return redirect('sliderimage_view')


# Reservation management Pages Start
@user_passes_test(is_admin, login_url='/login/')
def Customer_reservation(request):
    reserve = Reservation.objects.filter(res_status__in=['Disabled', 'Booked'])
    return render(request,'customer_reservation.html',{'reserve':reserve})


@user_passes_test(is_admin, login_url='/login/')
def Customer_reservation_approved(request,id):
    reserve = Reservation.objects.get(id=id)
    reserve.res_status = 'Booked'
    
    user_obj = User.objects.get(username=reserve.username)  # Replace 4 with the actual user ID

    # Convert the User object to a string (e.g., using the username)
    username_str = str(user_obj.username)

    name = reserve.username
    email = name.email
    room = reserve.r_id.r_no
    room_name = reserve.r_id.r_cat.rc_name
    
    reserve.save()  
        
    subject = 'Room Booking'
    message_lines = [
    username_str,
    'Your' +' ' +room +' '+ room_name + ' '+ 'room',
    'Has Been Booked.'
    ]
    message = '\n'.join(message_lines)
    from_email = 'eproject.apt@gmail.com'  # Replace with your Gmail email address
    recipient_list = [email]  # Replace with the recipient's email address

    send_mail(subject, message, from_email, recipient_list)

    return redirect('customer_reservation')

@user_passes_test(is_admin, login_url='/login/')
def Customer_reservation_reject(request,id):
    reserve = Reservation.objects.get(id=id)
    if request.method == 'POST':
        res_reason = request.POST.get('res_reason')
        username = reserve.username
        r_id = reserve.r_id
        check_in_date = reserve.check_in_date
        check_out_date = reserve.check_out_date
        email  =  reserve.username.email
        
        subject = 'ROOM REQUEST REJECTED'
        message = (res_reason)
        from_email = 'eproject.apt@gmail.com'  # Replace with your Gmail email address
        recipient_list = [email]  # Replace with the recipient's email address

        send_mail(subject, message, from_email, recipient_list)
        
        reject = Reservation_Reject(username=username, r_id=r_id,check_in_date=check_in_date,check_out_date=check_out_date,res_reason=res_reason)
        reject.save()
        
        reserve.delete()
        return redirect ('customer_reservation')
        
    return render (request,'reject_form.html',{'reserve':reserve})

@user_passes_test(is_admin, login_url='/login/')
def Customer_reservation_cancel(request):
    reserve = Reservation.objects.filter(res_status='Cancelled')
    return render(request,'Cancelled_reservation_pafe.html',{'reserve':reserve})

@user_passes_test(is_admin, login_url='/login/')
def Reservation_reject_page(request):
    reject = Reservation_Reject.objects.all().order_by('-id')
    return render(request,'Rejected_reservation.html',{'reject':reject})

# Reservation management Pages End

# Check Out Start
@user_passes_test(is_admin, login_url='/login/')
def Customer_check_out(request,id):
    reserve = Reservation.objects.get(id=id)
    
    username = reserve.username
    r_id = reserve.r_id
    check_in_date = reserve.check_in_date
    check_out_date = reserve.check_out_date
    
    check_out = Check_Out(username=username,r_id=r_id,check_in_date=check_in_date,check_out_date=check_out_date)
    check_out.save()
    
    reserve.delete()
    
    return redirect('customer_reservation')

@user_passes_test(is_admin, login_url='/login/')
def Customer_check_out_page(request):
    reserve = Check_Out.objects.all().order_by('-id')
    return render (request,'customer_checkout_Page.html',{'reserve':reserve})

# Check Out End


# Feed Back Start
@user_passes_test(is_admin, login_url='/login/')
def View_Feedback(request):
    feedback = Feedback.objects.filter(feedback_status__in=['False','True'])
    return render(request,'feedback_view.html',{'feedback':feedback})


@user_passes_test(is_admin, login_url='/login/')
def feedback_permission_page(request,id):
    feedback = Feedback.objects.get(id=id)
    
    if feedback.feedback_status == 'False':
        feedback.feedback_status = 'True'
        feedback.save()
        return redirect('feedback_view')
    
    if feedback.feedback_status == 'True':
        feedback.feedback_status = 'False'
        feedback.save()
        return redirect('feedback_view')
    
    
@user_passes_test(is_admin, login_url='/login/')
def feedback_delete_page(request,id):
    feedback = Feedback.objects.get(id=id)

    feedback.feedback_status = 'Delete'
    feedback.save()
    return redirect('feedback_view')

# Feedback end

    

    