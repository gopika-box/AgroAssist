from django.urls import path
from .views import farmer_dashboard

urlpatterns = [
    path('dashboard/',farmer_dashboard, name='farmer_dashboard'),
]