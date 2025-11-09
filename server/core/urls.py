"""
URL configuration for core app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, FeedbackViewSet

# Создаем роутер для ViewSets
router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'feedback', FeedbackViewSet, basename='feedback')

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
]
