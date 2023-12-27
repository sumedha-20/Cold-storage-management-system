from datetime import datetime
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from ColdStorage.models import *
from datetime import date

def home(request):
    data=ColdStorage.objects.all()
    return render(request,'home.html',locals())
def Signup_User(request):
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['address']
        user = User.objects.create_user(email=e, username=e, password=p, first_name=f, last_name=l)
        UserProfile.objects.create(user=user, contact=con, address=add)
        messages.success(request, "Registration Successful")
        return redirect('login')
    return render(request,'registration.html')
def Login_User(request):
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect('/')
        else:
            messages.success(request, "Invalid Username and password")
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('home')
@login_required(login_url='/login_admin/')
def admin_home(request):
    users = UserProfile.objects.all()
    users=users.count()
    storage = ColdStorage.objects.all()
    storage = storage.count()
    new = ApplicationForm.objects.filter(status="Not Updated Yet")
    new = new.count()
    accept = ApplicationForm.objects.filter(status="Accepted")
    accept = accept.count()
    reject = ApplicationForm.objects.filter(status="Rejected")
    reject = reject.count()
    total = ApplicationForm.objects.filter()
    total = total.count()

    return render(request,'admin_home.html',locals())
def Login_admin(request):
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect('admin_home')
        except:
            messages.success(request, "Invalid user")
    return render(request, 'admin_login.html')
@login_required(login_url='/login_admin/')
def add_storage(request):
    if request.method == 'POST':
        t = request.POST['title']
        l = request.POST['location']
        c = request.POST['cost']
        i = request.FILES['image']
        ColdStorage.objects.create(title=t, location=l, cost=c,image=i)
        messages.success(request, "Registration Successful")
        return redirect('admin_home')
    return render(request,'add_storage.html')
@login_required(login_url='/login_admin/')
def manage_storage(request):
    data=ColdStorage.objects.all()
    return render(request,'manage_storage.html',locals())
@login_required(login_url='/login_admin/')
def edit_storage(request,pid):
    data=ColdStorage.objects.get(id=pid)
    if request.method == 'POST':
        t = request.POST['title']
        l = request.POST['location']
        c = request.POST['cost']
        try:
            im = request.FILES['image']
            data.image = im
            data.save()
        except:
            pass
        data.title=t
        data.location=l
        data.cost=c
        data.save()
        messages.success(request, "Storage Detail Updated Successful")
        return redirect('manage_storage')
    return render(request, 'edit_storage.html',locals())
@login_required(login_url='/login_admin/')
def delete_storage(request,pid):
    data=ColdStorage.objects.get(id=pid)
    data.delete()
    messages.success(request, "deleted Successful")
    return redirect('manage_storage')
@login_required(login_url='/login/')
def apply_now(request,pid=None):
    if pid:
        data=ColdStorage.objects.get(id=pid)
    storage=ColdStorage.objects.all()
    user=UserProfile.objects.get(user=request.user)
    application_number = "%0.12d" % random.randint(0, 999999999999)
    if request.method == 'POST':
        s = request.POST['storage']
        t = request.POST['type']
        f = request.POST['from']
        to = request.POST['to']
        s=ColdStorage.objects.get(id=s)
        ApplicationForm.objects.create(user=user,storage=s,type=t,fromDate=f,toDate=to,applicationNumber=application_number,status="Not Updated Yet")
        messages.success(request, "Apply Request Sent Successfully")
        return redirect('view_booked_storage')
    return render(request,'apply_now.html',locals())
@login_required(login_url='/login/')
def view_booked_storage(request):
    user=UserProfile.objects.get(user=request.user)
    storage=ApplicationForm.objects.filter(user=user)
    return render(request,'view_booked_storage.html',locals())
@login_required(login_url='/login/')
def view_detail_booked_storage(request,pid):
    data = ApplicationForm.objects.get(id=pid)
    print(data.fromDate)
    sd=str(data.fromDate)
    ed=str(data.toDate)
    d1 = datetime.strptime(sd, "%Y-%m-%d")
    d2 = datetime.strptime(ed, "%Y-%m-%d")
    delta = d2 - d1
    days=delta.days
    cost=data.storage.cost
    totalcost=int(days)*int(cost)
    return render(request, 'view_detail_booked_storage.html', locals())
@login_required(login_url='/login_admin/')
def view_new_application_request(request):
    data=ApplicationForm.objects.filter(status="Not Updated Yet")
    return render(request,'view_new_application_request.html',locals())
@login_required(login_url='/login_admin/')
def admin_view_detail_booked_storage(request,pid):
    data = ApplicationForm.objects.get(id=pid)
    print(data.fromDate)
    sd=str(data.fromDate)
    ed=str(data.toDate)
    d1 = datetime.strptime(sd, "%Y-%m-%d")
    d2 = datetime.strptime(ed, "%Y-%m-%d")
    delta = d2 - d1
    days=delta.days
    return render(request, 'admin_view_detail_booked_storage.html', locals())
@login_required(login_url='/login_admin/')
def approve_request(request,pid):
    data=ApplicationForm.objects.get(id=pid)
    date=datetime.today()
    if request.method == "POST":
        r = request.POST['remark']
        s = request.POST['status']
        data.remark=r
        data.status=s
        data.remarkDate=date
        data.save()
        messages.success(request, "Application Status Updated Successful")
        return redirect('view_all_application_request')
    return render(request, 'approve_request.html', locals())
@login_required(login_url='/login_admin/')
def view_all_application_request(request):
    data=ApplicationForm.objects.filter()
    return render(request,'view_all_application_request.html',locals())
@login_required(login_url='/login_admin/')
def view_accepted_application_request(request):
    data=ApplicationForm.objects.filter(status="Accepted")
    return render(request,'view_accepted_application_request.html',locals())
@login_required(login_url='/login_admin/')
def view_rejected_application_request(request):
    data=ApplicationForm.objects.filter(status="Rejected")
    return render(request,'view_rejected_application_request.html',locals())
@login_required(login_url='/login_admin/')
def all_users(request):
    data=UserProfile.objects.all()
    return render(request,'all_users.html',locals())
@login_required(login_url='/login_admin/')
def find_by_date(request):
    t=''
    datef=''
    datet=''
    if request.method=='POST':
        datef=request.POST['datef']
        datet=request.POST['datet']
        try:
            t=ApplicationForm.objects.filter(applyDate__lte=datet,applyDate__gte=datef)
        except:
            t=None
    return render(request,'find_by_date.html',locals())
@login_required(login_url='/login_admin/')
def search_report(request):
    data=""
    empId=""
    if request.method=='POST':
        userinput=request.POST['userinput']
        print(userinput)
        try:
            data = ApplicationForm.objects.filter(Q(applicationNumber=userinput) | Q(status__contains=userinput) | Q(user__user__email__contains=userinput) | Q(user__contact__contains=userinput))
        except:
            data=None
        print(data)
    return render(request,'search_report.html',locals())
@login_required(login_url='/login/')
def user_Change_Password(request):
    user = User.objects.get(username=request.user.username)
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('user_Change_Password')

    return render(request,'user_change_password.html')
@login_required(login_url='/login_admin/')
def admin_Change_Password(request):
    user = User.objects.get(username=request.user.username)
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('admin_Change_Password')

    return render(request,'admin_change_password.html')
def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')
def gallery(request):
    return render(request,'gallery.html')
@login_required(login_url='/login/')
def edit_user(request):
    user=UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['address']
        user.user.first_name=f
        user.user.last_name=l
        user.user.email=e
        user.user.username=e
        user.contact=con
        user.address=add
        user.user.save()
        user.save()
        messages.success(request, "Update Successful")
        return redirect('/')
    return render(request,'edit_user.html',locals())
@login_required(login_url='/login_admin/')
def delete_user(request,pid):
    data=User.objects.get(id=pid)
    data.delete()
    messages.success(request, 'User Deleted Successfully')
    return redirect('all_users')
