"""
URL configuration for notifications app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

# Создаем роутер для ViewSets
router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

app_name = 'notifications'

urlpatterns = [
    path('', include(router.urls)),
]
