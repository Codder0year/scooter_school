from django.urls import path
from .views import trainers_list
from django.conf import settings
from django.conf.urls.static import static
app_name = 'trainers'

urlpatterns = [
    path('', trainers_list, name='trainers_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)