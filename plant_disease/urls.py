from django.urls import path
from .views import disease_predict

app_name = 'ml_model'
urlpatterns = [
    path('disease_predict/',disease_predict,name='disease_predict'),

]
