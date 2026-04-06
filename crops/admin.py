from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display=('name','season','soil_type')
    list_filter=('season',)
    search_fields=('name',)

@admin.register(Fertilizer)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'type')
    list_filter = ('type',)
    search_fields = ('name', 'brand')

@admin.register(CropFertilizerSchedule)
class CropFertilizerScheduleAdmin(admin.ModelAdmin):
    list_display = ('crop', 'fertilizer', 'stage', 'quantity')
    list_filter = ('crop', 'fertilizer')
    search_fields = ('stage',)