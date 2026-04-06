from django.urls import path
from . import views

app_name='doubts'
urlpatterns = [
    path('ask/', views.ask_doubt, name='ask_doubt'),
    path('my-doubts/', views.my_doubts, name='my_doubts'),
    path('officer-doubts/', views.officer_doubts, name='officer_doubts'),
    path('reply/<int:doubt_id>/', views.reply_doubt, name='reply_doubt'),
]
