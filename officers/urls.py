from django.urls import path
from .views import officers_dashboard

urlpatterns = [
    path('dashboard/',officers_dashboard, name='officers_dashboard'),
]