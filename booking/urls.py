from django.urls import path

from . import views
from .views import BookingCreateView
from django.views.generic import TemplateView

app_name = 'booking'

urlpatterns = [
    path('new/', BookingCreateView.as_view(), name='booking_new'),
    path('booking/success/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('get-trainer-courses/<int:trainer_id>/', views.get_trainer_courses, name='get_trainer_courses'),
    path('get-course-trainers/<int:course_id>/', views.get_course_trainers, name='get_course_trainers'),
]