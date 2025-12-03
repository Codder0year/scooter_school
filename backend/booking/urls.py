# booking/urls.py
from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.BookingCreateView.as_view(), name='booking_new'),
    path('get-trainer-courses/<int:trainer_id>/', views.get_trainer_courses, name='get_trainer_courses'),
    path('get-course-trainers/<int:course_id>/', views.get_course_trainers, name='get_course_trainers'),
    path('success/', views.BookingSuccessView.as_view(), name='booking_success'),
]