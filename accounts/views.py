from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import User, OfficerProfile

# Create your views here.
def landing_page(request):
    return render(request,'accounts/landing.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username,password=password)
        print("auth result:",user)
        if user is not None:
            login(request,user)

            if user.role =='farmer':
                return redirect('farmer_dashboard')
            elif user.role =='admin':
                return redirect('/admin/')
            elif user.role =='officer':
                if user.is_approved:
                    return redirect('officers_dashboard')
                else:
                    return redirect('pending_approval')
            
        else:
            return render(request, 'accounts/login.html', {'error':'Invalid username or password'})
        
    return render(request, 'accounts/login.html')

@login_required
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')
@login_required
def farmer_dashboard(request):
    return render(request, 'farmer/dashboard.html')
@login_required
def officer_dashboard(request):
    return render(request, 'officers/dashboard.html')

def pending_approval (request):
    return render(request,'officers/pending_approval.html')

def register(request):
    return render(request,'accounts/register.html')
    

def farmer_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            role='farmer',
            is_approved = True
        )
        return redirect('login')
    return render(request,'accounts/farmer_register.html')
    
def officer_register(request):
    if request.method == "POST":
        username = request.POST.get("uniqueId")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        panchayat = request.POST.get("panchayat")
        phone = request.POST.get("phone")

        if password != confirm_password:
            return render(request, 'accounts/officer_register.html',{
                'error': 'Passwords do not match'
            })
        if User.objects.filter(username=username).exists():
            return render(request,'accounts/officer_register.html',{
                'error':'Officer with this Unique ID already exists'
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            role='officer',
            is_approved = False
        )

        OfficerProfile.objects.create(
            user=user,
            unique_id = username,
            panchayat=panchayat,
            phone=phone
        )

        return redirect('login')
    return render(request, 'accounts/officer_register.html')

@staff_member_required
def officer_approval_dashboard(request):
    pending_officers = User.objects.filter(
        role='officer',
        is_approved = False
    )
    return render(
        request,
        'accounts/officer_approval_dashboard.html',
        {'officers': pending_officers}
    )

@staff_member_required
def approve_officer(request, user_id):
    officer = User.objects.get(id=user_id, role='officer')
    officer.is_approved = True
    officer.save()
    return redirect('officer_approval_dashboard')
