from django.urls import path, include

from . import views
from .views import home, AboutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('courses/', include('courses.urls')),
    path('contact/', views.contact_view, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)