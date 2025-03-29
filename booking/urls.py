from django.urls import path
from .views import BookingCreateView
from django.views.generic import TemplateView

app_name = 'booking'

urlpatterns = [
    path('new/', BookingCreateView.as_view(), name='booking_new'),
    path('success/', TemplateView.as_view(template_name='booking/success.html'), name='booking_success'),
]