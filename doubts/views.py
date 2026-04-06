from django.shortcuts import render, redirect, get_object_or_404
from .models import Doubt
from accounts.models import FarmerProfile, OfficerProfile
from django.contrib.auth.decorators import login_required

@login_required
def ask_doubt(request):
    farmer = Farmer.objects.get(user=request.user)
    officer = Officer.objects.get(panchayat=farmer.panchayat)

    if request.method == 'POST':
        Doubt.objects.create(
            farmer=farmer,
            officer=officer,
            panchayat=farmer.panchayat,
            title=request.POST['title'],
            description=request.POST['description'],
            image=request.FILES.get('image')
        )
        return redirect('my_doubts')

    return render(request, 'farmers/ask_doubt.html')

#farmer view doubt
@login_required
def my_doubts(request):
    farmer = request.user.farmer_profile
    doubts = Doubt.objects.filter(farmer=farmer)
    return render(request, 'farmers/view_doubts.html', {'doubts': doubts})

#view doubts
@login_required
def officer_doubts(request):
    officer = Officer.objects.get(user=request.user)
    doubts = Doubt.objects.filter(officer=officer)
    return render(request, 'officers/view_doubts.html', {'doubts': doubts})

@login_required
def reply_doubt(request, doubt_id):
    officer = Officer.objects.get(user=request.user)
    doubt = get_object_or_404(Doubt, id=doubt_id, officer=officer)

    if request.method == 'POST':
        Reply.objects.create(
            doubt=doubt,
            officer=officer,
            reply_text=request.POST['reply']
        )
        doubt.status = 'Replied'
        doubt.save()
        return redirect('officer_doubts')

    return render(request, 'officers/reply_doubts.html', {'doubt': doubt})
