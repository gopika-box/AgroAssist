from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import OfficerProfile
from .models import Government_scheme, Lesson, Course,SchemeApplication




@login_required
def officer_dashboard(request):
    if request.user.role != 'officer':
        return redirect('accounts:login')

    if not request.user.is_approved:
        return render(request, 'officers/pending_approval.html')

    return render(request, 'officers/dashboard.html' , {
        'courses_count': Course.objects.count(),
        'schemes_count': Government_scheme.objects.count(),
    }
    )



@login_required
def add_scheme(request):
    if request.user.role != 'officer':
        return redirect('accounts:login')

    if not request.user.is_approved:
        return redirect('accounts:pending_approval')

    if request.method == "POST":
        deadline = request.POST.get('deadline')
        Government_scheme.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            eligibility=request.POST.get('eligibility'),
            deadline=deadline if deadline else None,
            scheme_pdf=request.FILES.get('scheme_pdf'),
            uploaded_by=request.user
        )
        return redirect('officers:view_schemes')

    return render(request, 'officers/add_scheme.html')


@login_required
def view_schemes(request):
    schemes = Government_scheme.objects.all().order_by('deadline')

    # Officer view
    if request.user.role == 'officer':
        return render(request, 'officers/view_schemes.html', {
            'schemes': schemes
        })

    # Farmer view
    if request.user.role == 'farmer':
        return render(request, 'farmers/view_schemes.html', {
            'schemes': schemes
        })

    return redirect('accounts:login')

def apply_scheme(request, scheme_id):
    scheme = Government_scheme.objects.get(id=scheme_id)
    farmer = request.user
    farmer_profile = farmer.farmer_profile

    if request.method == "POST":

        # Find officer of same panchayat
        officer_profile = OfficerProfile.objects.filter(
            panchayat=farmer_profile.panchayat
        ).first()

        assigned_officer = officer_profile.user if officer_profile else None

        SchemeApplication.objects.create(
            scheme=scheme,
            farmer=farmer,
            phone=farmer_profile.phone,
            panchayat=farmer_profile.panchayat,
            land_area=request.POST.get('land_area'),
            notes=request.POST.get('notes'),
            assigned_officer=assigned_officer
        )

        return redirect("farmers:farmer_dashboard")

    return render(request, "farmers/apply_scheme.html", {
        "scheme": scheme,
        "farmer_profile": farmer_profile
    })

#Officer see the application
def officer_scheme_applications(request):
    applications = SchemeApplication.objects.filter(
        assigned_officer=request.user
    )
    return render(request, "officers/scheme_applications.html", {
        "applications": applications
    })

@login_required
def update_application_status(request, app_id, status):
    if request.user.role != 'officer':
        return redirect('accounts:login')
        
    # 1. Use get_object_or_404 to prevent crashes if the ID is wrong
    application = get_object_or_404(SchemeApplication, id=app_id)
    
    # 2. Update status (Ensure the strings match exactly what is in your template)
    application.status = status
    application.save()
    
    messages.success(request, f"Application {status} successfully!")

    # 3. CRITICAL: Add the 'officers:' namespace to the redirect
    return redirect("officers:officer_scheme_applications")

# MANAGE COURSE
#-----------------------
# =========================
# 📚 MANAGE COURSES (OFFICER)
# =========================
@login_required
def manage_courses(request):
    if request.user.role != 'officer':
        return redirect('accounts:login')

    # Only show courses created by this officer
    courses = Course.objects.filter(created_by=request.user)

    if request.method == 'POST':

        # ➕ ADD COURSE
        if 'add_course' in request.POST:
            title = request.POST.get('course_title')
            description = request.POST.get('course_description', '')

            if not title:
                messages.error(request, "Course title is required")
                return redirect('officers:manage_courses')

            Course.objects.create(
                title=title.strip(),
                description=description,
                created_by=request.user
            )

            messages.success(request, "Course added successfully")
            return redirect('officers:manage_courses')

        # ➕ ADD LESSON
        if 'add_lesson' in request.POST:

            lesson_type = request.POST.get('lesson_type')
            course_id = request.POST.get('course')
            title = request.POST.get('lesson_title')
            description = request.POST.get('description', '')

            video_url = None
            video_file = None
            notes_file = None

            # 🎥 VIDEO LESSON
            if lesson_type == "video":
                video_url = request.POST.get("video_url","").strip()
                video_file = request.FILES.get("video_file")

                if video_url:
                    video_url = video_url.strip()

                if not video_url and not video_file:
                    messages.error(request, "Provide YouTube URL or upload video")
                    return redirect('officers:manage_courses')

            # 📄 NOTES LESSON
            elif lesson_type == "notes":
                notes_file = request.FILES.get("notes_file")

                if not notes_file:
                    messages.error(request, "Upload notes file")
                    return redirect('officers:manage_courses')

            # VALIDATION
            if not course_id or not title:
                messages.error(request, "All required fields must be filled")
                return redirect('officers:manage_courses')

            Lesson.objects.create(
                course_id=course_id,
                title=title.strip(),
                lesson_type=lesson_type,
                video_url=video_url,
                video_file=video_file,
                notes_file=notes_file,
                description=description,
                uploaded_by=request.user
            )

            messages.success(request, "Lesson added successfully")
            return redirect('officers:manage_courses')

    return render(request, 'officers/manage_courses.html', {
        'courses': courses
    })


# =========================
# 👨‍🌾 VIEW COURSES (FARMER + OFFICER)
# =========================
@login_required
def farmer_view_courses(request):

    courses = Course.objects.all().order_by('created_at')

    # Select template based on role
    if request.user.role == 'officer':
        template = 'officers/view_courses.html'
    else:
        template = 'farmers/view_courses.html'

    return render(request, template, {
        'courses': courses
    })


# =========================
# 📖 VIEW LESSONS
# =========================
@login_required
def farmer_view_lessons(request, course_id):

    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('created_at')

    # Select template based on role
    if request.user.role == 'officer':
        template = 'officers/view_lessons.html'
    else:
        template = 'farmers/view_lessons.html'

    return render(request, template, {
        'course': course,
        'lessons': lessons
    })


# =========================
# 🏛 MODIFY GOVERNMENT SCHEME
# =========================
@login_required
def modify_scheme(request, scheme_id):
    if request.user.role != 'officer':
        return redirect('accounts:login')

    scheme = get_object_or_404(Government_scheme, id=scheme_id)

    # Only uploader can modify
    if scheme.uploaded_by != request.user:
        return redirect('accounts:login')

    if request.method == 'POST':

        # ✏️ UPDATE
        if 'update_scheme' in request.POST:
            scheme.title = request.POST.get('title', '').strip()
            scheme.description = request.POST.get('description', '')
            scheme.eligibility = request.POST.get('eligibility', '')
            scheme.deadline = request.POST.get('deadline')

            if request.FILES.get('scheme_pdf'):
                scheme.scheme_pdf = request.FILES.get('scheme_pdf')

            scheme.save()
            messages.success(request, "Scheme updated successfully")
            return redirect('officers:view_schemes')

        # ❌ DELETE
        if 'delete_scheme' in request.POST:
            scheme.delete()
            messages.success(request, "Scheme deleted successfully")
            return redirect('officers:view_schemes')

    return render(request, 'officers/modify_scheme.html', {
        'scheme': scheme
    })