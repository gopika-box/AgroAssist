from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view,name='login'),
    path('admin-dashboard/',admin_dashboard,name='admin_dashboard'),

    path('register/',register, name = 'register_option'),
    path('farmer_register/', farmer_register, name='farmer_register'),
    path('officer_register/',officer_register,name='officer_register'),

    path('farmer/dashboard/',farmer_dashboard,name='farmer_dashboard'),
    path('officer/dashboard/',officer_dashboard,name="officer_dashboard"),
    path('pending_approval/',pending_approval , name="pending_approval"),

    path('officer-approval/',officer_approval_dashboard,name='officer_approval_dashboard'),
    path('approve-officer/<int:user_id>/', approve_officer, name='approve_officer'),

]
