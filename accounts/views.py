from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from accounts.models import User, OfficerProfile,FarmerProfile

from marketplace.models import MarketplaceItem
from crops.models import Crop,CropFertilizerSchedule,Fertilizer
from officers.models import Course, Government_scheme,Lesson
from farmers.models import FarmerDoubt,ChatRoom,ChatMessage
from .utils import redirect_by_role

# -----------------------------
# Public Pages
# -----------------------------

def landing_page(request):
    return render(request, 'accounts/landing.html')

# -----------------------------
# Authentication
# -----------------------------

from django.contrib.auth.models import User

# Get the active User model (Custom or Default)
User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 1. Manually check if the user exists and is active
        try:
            # This will now work with your 'accounts.User' model
            user_to_check = User.objects.get(username=username)
            if not user_to_check.is_active:
                messages.error(request, "Your account has been blocked. Please contact the administrator.")
                return render(request, 'accounts/login.html')
        except User.DoesNotExist:
            pass

        # 2. Proceed with normal authentication
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect_by_role(user)
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')



@login_required
def logout_view(request):
    logout(request)
    return redirect('landing')


# -----------------------------
# Registration
# -----------------------------

def register(request):
    return render(request, 'accounts/register.html')


def farmer_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        panchayat = request.POST.get("panchayat")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation - check all required fields
        if not all([first_name, last_name, username, email, phone, panchayat, password, confirm_password]):
            messages.error(request, "All fields are required")
            return redirect('accounts:farmer_register')

        # Check password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('accounts:farmer_register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('accounts:farmer_register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('accounts:farmer_register')

        # Validate phone number
        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Enter a valid 10-digit phone number")
            return redirect('accounts:farmer_register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='farmer'
        )

        # Create farmer profile
        FarmerProfile.objects.create(
            user=user,
            phone=phone,
            panchayat=panchayat
        )

        messages.success(request, "Registration successful! You can now login.")
        return redirect('accounts:login')

    return render(request, 'accounts/farmer_register.html')

def officer_register(request):
    if request.method == "POST":
        unique_id = request.POST.get("uniqueId")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        panchayat = request.POST.get("panchayat")
        phone = request.POST.get("phone")

        # Validation - check all required fields
        if not all([unique_id, first_name, last_name, username, email, password, confirm_password, panchayat, phone]):
            messages.error(request, "All fields are required")
            return redirect('accounts:officer_register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('accounts:officer_register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('accounts:officer_register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('accounts:officer_register')

        # Check if unique_id already exists
        if OfficerProfile.objects.filter(unique_id=unique_id).exists():
            messages.error(request, "Officer with this Unique ID already exists")
            return redirect('accounts:officer_register')

        # Validate phone number
        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Enter a valid 10-digit phone number")
            return redirect('accounts:officer_register')

        # Create user with first_name and last_name
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='officer',
            is_approved=False
        )

        # Create officer profile
        OfficerProfile.objects.create(
            user=user,
            unique_id=unique_id,
            panchayat=panchayat,
            phone=phone
        )

        messages.success(
            request,
            "Registration submitted successfully. Awaiting admin approval."
        )
        return redirect('accounts:login')

    return render(request, 'accounts/officer_register.html')

def customer_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        if not all([username, email, password, phone]):
            messages.error(request, "All fields are required")
            return redirect('accounts:customer_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('accounts:customer_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('accounts:customer_register')

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Enter a valid 10-digit phone number")
            return redirect('accounts:customer_register')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect('accounts:customer_register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='customer',
            is_approved=True
        )

        messages.success(request, "Customer registration successful. Please login.")
        return redirect('accounts:login')

    return render(request, 'accounts/customer_register.html')


# -----------------------------
# Pending Approval Page
# -----------------------------

@login_required
def pending_approval(request):
    return render(request, 'officers/pending_approval.html')


@staff_member_required
def officer_approval_dashboard(request):
    pending_officers = User.objects.filter(
        role='officer',
        is_approved=False
    ).select_related('officer_profile')
    return render(
        request,
        'admin/officer_approval_dashboard.html',
        {'officers': pending_officers}
    )

@staff_member_required
def approve_officer(request, user_id):
    officer = get_object_or_404(User, id=user_id, role='officer')
    officer.is_approved = True
    officer.save()

    messages.success(request, "Officer approved successfully")
    return redirect('accounts:officer_approval_dashboard')

@staff_member_required
def reject_officer(request, officer_id):
    officer = get_object_or_404(User, id=officer_id)
    officer.delete()  # or mark rejected instead
    return redirect('accounts:officer_approval_dashboard')


# -----------------------------
# Admin dashboard
# -----------------------------
@login_required
@admin_required
def admin_dashboard(request):
    context = {
        'total_farmers': User.objects.filter(role='farmer').count(),
        'total_officers': User.objects.filter(role='officer').count(),
        'pending_officers': User.objects.filter(role='officer', is_approved=False).count(),
        'total_listings': MarketplaceItem.objects.count(),
        'total_queries': FarmerDoubt.objects.count(),
    }

    return render(request, 'admin/dashboard.html', context)

@login_required
@admin_required
def admin_officers(request):
    officers = User.objects.filter(role='officer')
    return render(request, 'admin/officers.html', {
        'officers': officers
    })

@login_required
@admin_required
def admin_users(request):
    farmers = User.objects.filter(role='farmer')
    return render(request,'admin/users.html',{'users':farmers
    })
@login_required
@admin_required
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    
    # Prevent admin from deleting themselves
    if user_to_delete == request.user:
        messages.error(request, "You cannot delete your own account from here.")
    else:
        user_to_delete.delete()
        messages.success(request, f"User {user_to_delete.username} has been deleted.")
        
    return redirect('accounts:admin_users')
@staff_member_required
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Prevent admin from disabling themselves
    if user == request.user:
        return redirect('accounts:admin_users')

    user.is_active = not user.is_active
    user.save()

    return redirect('accounts:admin_users')
@login_required
@admin_required
def admin_crops(request):
    crops =  Crop.objects.all().order_by('season','name')
    return render(request,'admin/admin_crops.html',{'crops':crops})

@login_required
@admin_required
def admin_add_crop(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Crop.objects.filter(name__iexact = name).exists():
            messages.error(request,"This crop already exisits")
            return redirect('accounts:admin_add_crop')
        season = request.POST.get('season')
        soil_type = request.POST.get('soil_type')
        duration = request.POST.get('duration')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        new_crop = Crop.objects.create(
            name=name,
            season=season,
            soil_type=soil_type,
            duration=duration,
            description=description,
            image=image
        )

        # 🔥 REDIRECT TO ADD SCHEDULE FOR THIS CROP
        return redirect('accounts:add_fertilizer_schedule', crop_id=new_crop.id)

    return render(request, 'admin/admin_add_crop.html')

@login_required
@admin_required
def add_fertilizer_schedule(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    fertilizers = Fertilizer.objects.all()

    if request.method == "POST":

        fertilizers_list = request.POST.getlist('fertilizer[]')
        stages = request.POST.getlist('stage[]')
        quantities = request.POST.getlist('quantity[]')
        notes_list = request.POST.getlist('notes[]')

        for i in range(len(fertilizers_list)):
            CropFertilizerSchedule.objects.create(
                crop=crop,
                fertilizer_id=fertilizers_list[i],
                stage=stages[i],
                quantity=quantities[i],
                notes=notes_list[i]
            )

        return redirect('accounts:admin_crops')

    return render(request, 'admin/add_fertilizer_schedule.html', {
        'crop': crop,
        'fertilizers': fertilizers
    })

@login_required
@admin_required
def admin_delete_crop(request,crop_id):
    if request.method == "POST":
        Crop.objects.filter(id=crop_id).delete()
    return redirect('accounts:admin_crops')


def add_schedule(request):
    crops = Crop.objects.all()
    fertilizers = Fertilizer.objects.all()

    if request.method == "POST":
        CropFertilizerSchedule.objects.create(
            crop_id=request.POST.get('crop'),
            fertilizer_id=request.POST.get('fertilizer'),
            stage=request.POST.get('stage'),
            quantity=request.POST.get('quantity'),
            notes=request.POST.get('notes')
        )
        return redirect('accounts:admin_crops')  # ✅ redirect after save

    return render(request, 'admin/add_schedule.html', {
        'crops': crops,
        'fertilizers': fertilizers
    })

#ADMIN COURSE MANAGE
@login_required
@admin_required
def admin_courses(request):
    courses=Course.objects.all().order_by('-id')
    return render(request,'admin/admin_course.html',{'courses':courses})



@login_required
@admin_required
def admin_edit_course(request,course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        course.title= request.POST.get('title')
        course.description = request.POST.get('description')
        course.save()

        return redirect('accounts:admin_courses')
    return render(request,'admin/admin_edit_course.html',{'course':course})

@login_required
@admin_required
def admin_delete_course(request,course_id):
    if request.method == 'POST':
        Course.objects.filter(id=course_id).delete()

    return redirect('accounts:admin_courses')


def manage_classes(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Order lessons by ID or a 'position' field if you have one
    lessons = course.lessons.all().order_by('id')

    return render(request, 'admin/manage_classes.html', {
        'course': course,
        'lessons': lessons
    })

def edit_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        # 1. Update basic text fields
        lesson.title = request.POST.get("title")
        lesson.lesson_type = request.POST.get("lesson_type")
        lesson.content = request.POST.get("content") # This is the description/notes text

        # 2. Handle Video Logic
        if lesson.lesson_type == "video":
            lesson.video_url = request.POST.get("video_url")
            if 'video_file' in request.FILES:
                lesson.video_file = request.FILES['video_file']
        
        # 3. Handle PDF/Notes Logic
        elif lesson.lesson_type == "notes":
            if 'notes_file' in request.FILES:
                lesson.notes_file = request.FILES['notes_file']

        lesson.save()
        messages.success(request, "Lesson updated successfully!")
        return redirect('accounts:manage_classes', course_id=lesson.course.id)

    return render(request, 'admin/edit_lesson.html', {'lesson': lesson})

def delete_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    course_id = lesson.course.id
    lesson.delete()
    return redirect('manage_classes', course_id=course_id)

#------SCHEMES--------
@login_required
@admin_required
def admin_schemes(request):
    schemes = Government_scheme.objects.all().order_by('-created_at')
    return render(request, "admin/admin_schemes.html", {"schemes": schemes})


@login_required
@admin_required
def admin_delete_scheme(request, scheme_id):
    if request.method == "POST":
        Government_scheme.objects.filter(id=scheme_id).delete()
    return redirect("accounts:admin_schemes")






# -----------------------------
# CUSTOMER
# -----------------------------
@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('accounts:login')

    return render(request, 'customer/dashboard.html')
