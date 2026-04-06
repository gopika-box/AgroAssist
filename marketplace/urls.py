from django.urls import path
from .views import *

app_name = 'marketplace'
urlpatterns = [
    path('add/',add_item,name='add_item'),
    path('view/',view_items,name='view_items'),
    path('delete/<int:item_id>/', delete_item, name='delete_item'),
    path('edit/<int:item_id>/', edit_item, name='edit_item'),

]
