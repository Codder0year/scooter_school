from rest_framework import routers
from django.urls import path, include
from .views import NewsViewSet, contact_view

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', contact_view, name='core-contact'),  # POST endpoint для формы контакта
]
