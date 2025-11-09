"""
URL configuration for courses app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    CourseViewSet,
    LessonViewSet,
    AssignmentViewSet,
    SubmissionViewSet,
    GradeViewSet,
)

# Создаем роутер для ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'submissions', SubmissionViewSet, basename='submission')
router.register(r'grades', GradeViewSet, basename='grade')

app_name = 'courses'

urlpatterns = [
    path('', include(router.urls)),
]
