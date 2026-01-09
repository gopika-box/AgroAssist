from django.contrib import admin
from .models import User,OfficerProfile

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('username','role','is_approved','is_active')
    list_filter=('role','is_approved')
    search_fields=('username',)
    list_editable=('is_approved',)

@admin.register(OfficerProfile)
class OfficerProfileAdmin(admin.ModelAdmin):
    list_display=('user','unique_id','panchayat','phone')
    search_fields=('username','panchayat')
    
