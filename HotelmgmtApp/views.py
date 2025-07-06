from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room_cat,Add_room
from .form import  RoomcatForm, AddRoom_Form
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test




def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin, login_url='/login/')
def Roomcat_page(request):
    if request.method == 'POST':
        form = RoomcatForm(request.POST)
        if form.is_valid():     
            rc_name = form.cleaned_data.get('rc_name')
            rc_des = form.cleaned_data.get('rc_des')
            
            room_cat = Room_cat(rc_name = rc_name, rc_des = rc_des)
            room_cat.save()
            return redirect('cat_list')
    return render(request,'room_category.html')


@user_passes_test(is_admin, login_url='/login/')
def Roomcat_list(request):
    rc = {}
    
    rc["dataset"] = Room_cat.objects.all()
    return render(request,'category_list.html',rc)


@user_passes_test(is_admin, login_url='/login/')
def Roomcat_edit(request,id):
    rc_edit = Room_cat.objects.get(id=id)
    
    if request.method == 'POST':
        rc_edit.rc_name = request.POST.get('rc_name')
        rc_edit.rc_des = request.POST.get('rc_des')
        rc_edit.save()
        return redirect('cat_list')
    
    return render(request,'rc_edit.html',{'rc_edit': rc_edit})


@user_passes_test(is_admin, login_url='/login/')
def Roomcat_delete(request,id):
    rc_del = Room_cat.objects.get(id=id)
    rc_del.delete()
    return redirect('cat_list') 



@user_passes_test(is_admin, login_url='/login/')
def Addroom_page(request):
    if request.method == 'POST':
        form = AddRoom_Form(request.POST, request.FILES)
        if form.is_valid():
            r_no = form.cleaned_data.get('r_no')
            r_bed_no = form.cleaned_data.get('r_bed_no')
            r_cat = form.cleaned_data.get('r_cat')
            r_capacity = form.cleaned_data.get('r_capacity')
            r_price =form.cleaned_data.get('r_price')
            room_img = form.cleaned_data.get('room_img')
            
            room_category = Room_cat.objects.get(id = r_cat)
            
            add_room = Add_room(r_no=r_no, r_bed_no= r_bed_no, r_cat= room_category, room_img = room_img, r_capacity=r_capacity,r_price=r_price )
            add_room.save()
            return redirect('room_view')
            
    op =  Room_cat.objects.all()
    context = {'Category':op}
    form = RoomcatForm()
    return render(request,'add_room.html',context)     

@user_passes_test(is_admin, login_url='/login/')
def room(request):
    total_records = Add_room.objects.count()
    
    room_data = Add_room.objects.all()
    context ={'room_data':room_data, 'total_records':total_records}
    return render(request, 'room.html', context)



@user_passes_test(is_admin, login_url='/login/')
def Room_edit(request, id):
    r_edit = Add_room.objects.get(id=id)

    if request.method == 'POST':
        r_edit.r_no = request.POST.get('r_no')
        r_edit.r_bed_no = request.POST.get('r_bed_no')

        # Get the Room_cat instance based on the submitted value
        r_cat_id = request.POST.get('r_cat')
        r_cat_instance = Room_cat.objects.get(pk=r_cat_id)
        r_edit.r_cat = r_cat_instance

        # Assuming you have a form to handle image uploads
        form = AddRoom_Form(request.POST, request.FILES)
        if form.is_valid():
            r_edit.room_img = form.cleaned_data['room_img']

        r_edit.save()
        return redirect('room_view')
    else:
        form = AddRoom_Form()

    op = Room_cat.objects.all()
    context = {'Category': op, 'form': form, 'r_edit': r_edit}
    return render(request, 'room_edit.html', context)


@user_passes_test(is_admin, login_url='/login/')
def Room_delete(request,id):
    r_del = Add_room.objects.get(id=id)
    r_del.delete()
    return redirect('room_view') 
















# def Roomcat_page(request):
#     if request.method == 'POST':
#         form = Roomcat_Form(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     form = Roomcat_Form()
#     return render(request,'room_cat.html',{'form': form})

           