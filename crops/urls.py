from django.urls import path
from .views import *
app_name = "crops"
urlpatterns = [
path('list_crops/',seasonal_crops,name='seasonal_crops'),
path('plant-disease',plant_disease,name='plant_disease')
]
