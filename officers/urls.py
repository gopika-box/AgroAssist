from django.urls import path
from .views import *
from farmers.views import officer_doubts,reply_doubt

app_name = 'officers'


urlpatterns = [
    path('dashboard/',officer_dashboard, name='officer_dashboard'),
    path('add-scheme/', add_scheme, name='add_scheme'),
    path('view_schemes/', view_schemes, name='view_schemes'),

    path('manage-courses/',manage_courses,name='manage_courses'),
    path('courses/',farmer_view_courses,name='farmer_view_courses'),
    path( 'courses/<int:course_id>/lessons/', farmer_view_lessons,name='farmer_view_lessons'),
    path('schemes/modify/<int:scheme_id>/', modify_scheme, name='modify_scheme'),

    # Farmer applies
    path("schemes/apply/<int:scheme_id>/",apply_scheme,name="apply_scheme"),
    # Officer views applications
    path("officer/scheme-applications/",officer_scheme_applications,name="officer_scheme_applications"),
    # Approve / Reject
    path("officer/application/<int:app_id>/<str:status>/",update_application_status,name="update_application_status"),

    path('doubts/', officer_doubts, name='doubts'),
    path('doubts/reply/<int:doubt_id>/', reply_doubt, name='reply_doubt'),


]