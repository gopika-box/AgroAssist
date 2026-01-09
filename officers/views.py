from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def officers_dashboard(request):
    if not request.user.is_approved:
        return render(request,'officers/pending_approval.html')
    
    return render(request,'officers/dashboard.html')