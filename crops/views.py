from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Crop

@login_required
def seasonal_crops(request):
    season = request.GET.get('season')

    crops = Crop.objects.prefetch_related(
        'cropfertilizerschedule_set__fertilizer'
    )

    if season:
        crops = crops.filter(season=season)

    # Officer view
    if request.user.role == 'officer':
        return render(request, 'officers/seasonal_crop.html', {
            'crops': crops,
            'selected_season': season
        })

    # Farmer view
    if request.user.role == 'farmer':
        return render(request, 'farmers/seasonal_crops.html', {
            'crops': crops,
            'selected_season': season
        })
    
    if request.user.role == 'admin':
        return render(request, 'admin/seasonal_crops.html', {
            'crops': crops,
            'selected_season': season
        })

    # Fallback (admin or unknown role)
    return render(request, 'accounts/login.html')

def plant_disease(request):
    # Officer view
    if request.user.role == 'officer':
        return render(request, 'officers/plant_disease.html')

    # Farmer view
    if request.user.role == 'farmer':
        return render(request, 'farmers/plant_disease.html')
    
    if request.user.role == 'admin':
        return render(request, 'admin/plant_disease.html')
    