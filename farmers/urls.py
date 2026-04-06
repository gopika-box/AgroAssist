from django.urls import path
from .views import *

app_name='farmers'

urlpatterns = [
    path('dashboard/',farmer_dashboard, name='farmer_dashboard'),
    path('courses/',farmer_view_courses,name='farmer_view_courses'),
    path('view_lessons',view_lessons,name='view_lessons'),
    path('ask-doubt/', ask_doubt, name='ask_doubt'),
    path('my-doubts/', my_doubts, name='my_doubts'),

    path('chat/start/<int:item_id>/', start_chat, name='start_chat'),
    path('chat/<int:room_id>/', chat_room, name='chat_room'),
    path('chat/<int:room_id>/block/', block_customer, name='block_customer'),
    path('chat/<int:room_id>/toggle-block/', toggle_block_customer, name='toggle_block_customer'),
    path('chats/', farmer_chats, name='farmer_chats'),
    path('customer/chats/', customer_chats, name='customer_chats'),

    path("my-applications/",my_applications,name="my_applications")


]