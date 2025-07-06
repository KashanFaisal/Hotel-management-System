
from django.contrib import admin
from django.urls import path
from main import views as main
from AdminApp import views 
from HotelmgmtApp import views as hotelmgmt
from UserApp import views as userapp
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Main
    path('contact_us/',main.Contact_page,name='contact_us'),
    
    
    #AdminApp
    # Dashboard 
    path('dashboard/', views.dashboard,name = 'dashboard'),
    
    # Employee Register And Login
    path('employee_register/', views.Employee_register.as_view(), name='employee_register'),
    path('login/', views.login_page, name='login'),
    path('logout_employee',views.logout_employee_page,name='logout_employee'),
    
    # Customer View and Approved Request    
    path('customer_view/', views.Customer_view,name = 'customer_view'),
    path('customer_list/', views.Customer_list_page,name = 'customer_list'),
    path('approve/<int:id>', views.Approve, name = 'approve'),

    # Admin Profile
    path('profile/',views.Profile_page, name = 'profile'),
    path('profile_edit/<str:name>',views.ProfileEdit_page, name = 'profile'),
    
    # Add Slider Image, Slider Image View, Enable Slider Image 
    path('slider_image/',views.SliderImage_Page, name = 'slider_image'),
    path('sliderimage_view/',views.SliderImage_View_Page, name = 'sliderimage_view'),
    path('sliderimage_enable/<int:id>',views.SliderImage_Enable, name = 'sliderimage_enable'),
    
    # View Customer Reservation, Approve Reservation, Reject Reservation
    path('customer_reservation/',views.Customer_reservation, name = 'customer_reservation'),
    path('customer_reservation_approved/<int:id>',views.Customer_reservation_approved, name = 'customer_reservation_approved'),
    path('customer_reservation_reject/<int:id>',views.Customer_reservation_reject, name = 'customer_reservation_reject'),
    
    # View Rejected Reservation
    path('rejected/', views.Reservation_reject_page,name='rejected'),
    
    # Check Out
    path('check_out/<int:id>', views.Customer_check_out,name = 'check_out'),
    path('check_out_Page/', views.Customer_check_out_page,name = 'check_out_Page'),
    
    # Canclled Reservation from User Side 
    path('cancell_reservation/', views.Customer_reservation_cancel,name='cancell_reservation'),
    
    # Feedback View, Manage View , Delete View
    path('feedback_view/',views.View_Feedback,name='feedback_view'),
    path('feedback_permission/<int:id>',views.feedback_permission_page,name='feedback_permission'),
    path('feedback_delete/<int:id>',views.feedback_delete_page,name='feedback_delete'),

    
    #HotlemgmtApp
    
    #Room Category 
    path('room_cat/', hotelmgmt.Roomcat_page, name= 'room_cat'),
    path('cat_list/', hotelmgmt.Roomcat_list,name='cat_list'),
    path('Roomcat_edit/<int:id>',hotelmgmt.Roomcat_edit,name='Roomcat_edit'),
    path('roomcat_delete/<int:id>', hotelmgmt.Roomcat_delete, name='roomcat_delete'),
    
    #Room
    path('add_room/', hotelmgmt.Addroom_page, name= 'add_room'),  
    path('room_view/', hotelmgmt.room, name= 'room_view'),
    path('room_edit/<int:id>', hotelmgmt.Room_edit,name='room_edit'),
    path('room_delete/<int:id>', hotelmgmt.Room_delete,name='room_delete'),
    
    
    
    #UserApp
    
    
    # User Index Page
    path('home/', userapp.index_page,name = 'home'),
    
    
    #  Customer Registeration, Login And Logout 
    path('customer_register/', userapp.Customer_register.as_view(), name='customer_register'),
    path('customer_login/', userapp.login_page, name='customer_login'),
    path('logout/', userapp.logout_page, name='logout'),
    
    
    # View Room, Signle page View ,Book Room, Search Room,
    path('room/', userapp.Room_display, name='room'),
    path('sig_room/<int:id>',userapp.singl_room,name='sig_room'),
    path('reservation/<int:id>', userapp.Reservation_page, name='reservation'),
    path('room_check/',userapp.check_availability, name='room_check'),
    
    # User Profile, edit Profile
    path('u_profile/',userapp.Profile_page, name='u_profile'),
    path('u_profile_edit/<str:name>',userapp.ProfileEdit_page, name='u_profile_edit'),
        
    # View Booking Detail And Cancell Booking
    path('booked_detail/',userapp.Customer_Book_Detail, name='booked_detail'),
    path('reservation_cancel/<int:id>', userapp.Customer_reservation_cancel,name='reservation_cancel'),
    
    # Feedback
    path('feedback/',userapp.Feedback_page,name='feedback'),
    
    # About
    path('about/',userapp.About_page,name='about'),
    





    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)