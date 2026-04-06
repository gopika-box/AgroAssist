from django.urls import path
from .views import *

app_name="accounts"

urlpatterns = [
    
    path('login/', login_view,name='login'),
    

    path('register/',register, name = 'register_option'),
    path('farmer_register/', farmer_register, name='farmer_register'),
    path('officer_register/',officer_register,name='officer_register'),
    path('customer_register/', customer_register, name='customer_register'),

    
    path('pending_approval/',pending_approval , name="pending_approval"),
    path('officer-approval/',officer_approval_dashboard,name='officer_approval_dashboard'),
    path('approve-officer/<int:user_id>/', approve_officer, name='approve_officer'),
     path('reject-officer/<int:officer_id>/', reject_officer, name='reject_officer'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),

    path('customer/dashboard/', customer_dashboard, name='customer_dashboard'),
    


    path('admin/officers/', admin_officers, name='admin_officers'),
    path('admin/users/', admin_users, name='admin_users'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('toggle-user/<int:user_id>/', toggle_user_status, name='toggle_user'),
    path('admin/crops/',admin_crops,name='admin_crops'),
    path('admin/crops/add/',admin_add_crop, name='admin_add_crop'),
    path('admin/crops/delete/<int:crop_id>/', admin_delete_crop, name='admin_delete_crop'),
    path('add-fertilizer/<int:crop_id>/', add_fertilizer_schedule, name='add_fertilizer_schedule'),
    path('admin/courses/',admin_courses,name='admin_courses'),
    path('admin/courses/edit/<int:course_id>',admin_edit_course,name='admin_edit_course'),
    path('admin/course/delete/<int:course_id>',admin_delete_course,name='admin_delete_course'),
    path('admin/courses/<int:course_id>/classes/', manage_classes, name='manage_classes'),
    path('admin/lessons/<int:lesson_id>/edit/', edit_lesson, name='edit_lesson'),
    path("admin/schemes/", admin_schemes, name="admin_schemes"),
    path("admin/schemes/delete/<int:scheme_id>/", admin_delete_scheme, name="admin_delete_scheme"),




    path('logout/',logout_view,name='logout'),
]
