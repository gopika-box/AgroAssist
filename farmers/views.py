from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from officers.models import Government_scheme, Lesson,Course,SchemeApplication
from marketplace.models import MarketplaceItem
from .models import FarmerDoubt,ChatRoom,ChatMessage,User,BlockList
from django.contrib import messages

# Create your views here.
@login_required
def farmer_dashboard(request):
    if request.user.role != 'farmer':
        return redirect('accounts:login')
    
    user = request.user

    #Stat
    from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from officers.models import SchemeApplication, Government_scheme

@login_required
def farmer_dashboard(request):
    user = request.user

    # Stats
    my_applications = SchemeApplication.objects.filter(farmer=user).count()
    pending = SchemeApplication.objects.filter(farmer=user, status="Pending").count()
    approved = SchemeApplication.objects.filter(farmer=user, status="Approved").count()

    # Latest schemes
    latest_schemes = Government_scheme.objects.order_by('-created_at')[:3]

    # Recent applications
    my_apps = SchemeApplication.objects.filter(
        farmer=user
    ).order_by('-created_at')[:5]

    context = {
        "my_applications": my_applications,
        "pending": pending,
        "approved": approved,
        "latest_schemes": latest_schemes,
        "my_apps": my_apps,
    }

    return render(request, "farmers/dashboard.html", context)



@login_required
def my_applications(request):
    applications = SchemeApplication.objects.filter(farmer = request.user).order_by('-created_at')

    return render(request, "farmers/my_applications.html",{
        "applications":applications
    })

@login_required
def view_lessons(reqeust):
    lessons = Lesson.objects.all().order_by('-created_at')
    return render(reqeust, 'farmers/view_lessons.html',{
        'lessons':lessons
    })

@login_required
def farmer_view_courses(request):
    if request.user.role !='farmer':
        return redirect('accounts:login')
    courses = Course.objects.all().order_by('created_at')
    return render(request,'farmers/view_courses.html',{
        'courses':courses
    })

#-----------
#DOUBTS
#-----------
@login_required
def ask_doubt(request):
    if request.user.role != 'farmer':
        return redirect('landing')

    farmer_profile = request.user.farmer_profile
    panchayat = farmer_profile.panchayat

    officer = User.objects.filter(
        role='officer',
        officer_profile__panchayat=panchayat,
        is_approved=True
    ).first()

    if not officer:
        messages.error(request, "No agricultural officer assigned to your panchayat.")
        return redirect('farmers:dashboard')

    if request.method == "POST":
        question = request.POST.get("question")

        if not question:
            messages.error(request, "Please enter your doubt")
            return redirect('farmers:ask_doubt')

        FarmerDoubt.objects.create(
            farmer=request.user,   # ✅ consistent
            officer=officer,
            panchayat=panchayat,
            question=question
        )

        messages.success(request,
    f"✅ Your doubt has been sent to Krishi Officer "
    f"{officer.username} ({panchayat} Panchayat). "
    f"You will receive a reply soon."
)
        return redirect('farmers:my_doubts')

    return render(request, 'farmers/ask_doubt.html')


@login_required
def my_doubts(request):
    if request.user.role != 'farmer':
        return redirect('landing')

    doubts = FarmerDoubt.objects.filter(farmer=request.user)
    return render(request, 'farmers/view_doubts.html', {
        'doubts': doubts
    })

@login_required
def officer_doubts(request):
    if request.user.role != 'officer':
        return redirect('landing')

    officer_profile = request.user.officer_profile

    doubts = FarmerDoubt.objects.filter(
        officer=request.user,
        panchayat=officer_profile.panchayat
    )

    return render(request, 'officers/view_doubts.html', {
        'doubts': doubts
    })


@login_required
def reply_doubt(request, doubt_id):
    doubt = FarmerDoubt.objects.get(id=doubt_id)

    if request.user != doubt.officer:
        return redirect('landing')

    if request.method == "POST":
        reply = request.POST.get("reply")

        if reply:
            doubt.reply = reply
            doubt.is_resolved = True
            doubt.replied_at = now()
            doubt.save()

            messages.success(request, "Reply sent to farmer.")
            return redirect('officers:doubts')

    return render(request, 'officers/reply_doubts.html', {
        'doubt': doubt
    })

@login_required
def start_chat(request, item_id):
    item = get_object_or_404(MarketplaceItem, id=item_id)

    # Only customers can start chat
    if request.user.role != 'customer':
        return redirect('accounts:login')

    farmer = item.user
    customer = request.user

    room, created = ChatRoom.objects.get_or_create(
        customer=customer,
        farmer=farmer,
        item=item
    )

    return redirect('farmers:chat_room', room_id=room.id)


@login_required
def chat_room(request, room_id):
    # 1. Fetch the chat room or return 404
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # 2. Security Check: Allow only the specific customer and farmer assigned to this room
    if request.user != room.customer and request.user != room.farmer:
        # Redirect to a safe page if an unauthorized user tries to access the room
        return redirect('landing')

    # 3. Check Block Status: Is the customer blocked by this farmer?
    is_blocked = BlockList.objects.filter(
        blocker=room.farmer, 
        blocked_user=room.customer
    ).exists()

    # 4. Handle Message Submission (POST)
    if request.method == "POST":
        # Block Logic: Prevent message creation if the block is active
        if is_blocked:
            # Optionally: messages.error(request, "This chat is currently locked.")
            return redirect('farmers:chat_room', room.id)

        msg = request.POST.get("message")
        if msg:
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                message=msg
            )
            # Update the room's 'updated_at' timestamp for sorting in the chat list
            room.save()
            
        return redirect('farmers:chat_room', room.id)

    # 5. Fetch all messages in chronological order
    messages = room.messages.order_by('timestamp')

    # 6. Choose Template & Context based on User Role
    if request.user.role == 'customer':
        template = 'customer/chat_room.html'
    else:
        template = 'farmers/chat_room.html'

    context = {
        'room': room,
        'messages': messages,
        'is_blocked': is_blocked,
    }

    return render(request, template, context)

@login_required
def block_customer(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Only the farmer in this room can block the customer
    if request.user == room.farmer:
        BlockList.objects.get_or_create(blocker=room.farmer, blocked_user=room.customer)
    
    return redirect('farmers:chat_room', room_id=room.id)

@login_required
def toggle_block_customer(request, room_id):
    if request.method == "POST":
        room = get_object_or_404(ChatRoom, id=room_id)
        
        if request.user == room.farmer:
            # Look for an existing block
            block_entry = BlockList.objects.filter(blocker=room.farmer, blocked_user=room.customer)
            
            if block_entry.exists():
                block_entry.delete() # Unblock
            else:
                BlockList.objects.create(blocker=room.farmer, blocked_user=room.customer) # Block
            
        return redirect('farmers:chat_room', room_id=room.id)
    return redirect('farmers:chat_room', room_id=room_id)

@login_required
def farmer_chats(request):
    rooms = ChatRoom.objects.filter(farmer=request.user).order_by('-updated_at')
    return render(request, 'farmers/chats.html', {
        'rooms': rooms
    })
@login_required
def customer_chats(request):
    if request.user.role != 'customer':
        return redirect('landing')

    rooms = ChatRoom.objects.filter(customer=request.user).order_by('-updated_at')

    return render(request, 'customer/chats.html', {
        'rooms': rooms
    })