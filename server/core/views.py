from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Feedback
from .serializers import CommentSerializer, FeedbackSerializer
from .tasks import send_comment_notification
from courses.models import Course, Lesson
from users.models import User


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления комментариями.
    
    - list: список комментариев
    - retrieve: детали комментария
    - create: создание комментария
    - update/partial_update: обновление комментария (только автор)
    - destroy: удаление комментария (только автор)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по типу контента и ID объекта
        content_type_id = self.request.query_params.get('content_type', None)
        object_id = self.request.query_params.get('object_id', None)
        
        if content_type_id and object_id:
            queryset = queryset.filter(
                content_type_id=content_type_id,
                object_id=object_id
            )
        
        # Фильтрация по родительскому комментарию (для получения ответов)
        parent_id = self.request.query_params.get('parent', None)
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        elif parent_id is None and self.request.query_params.get('top_level') == 'true':
            # Только комментарии верхнего уровня (без родителя)
            queryset = queryset.filter(parent__isnull=True)
        
        return queryset.select_related('author', 'parent').prefetch_related('replies')
    
    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Отправляем уведомление о новом комментарии
        send_comment_notification.delay(comment.id)
    
    def perform_update(self, serializer):
        serializer.save(is_edited=True)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            # Только автор может редактировать/удалять свои комментарии
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {'detail': 'Вы можете редактировать только свои комментарии.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {'detail': 'Вы можете удалять только свои комментарии.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    ViewSet для обратной связи.
    
    - list: список обратной связи (только для админов, пользователи видят только свои)
    - retrieve: детали обратной связи
    - create: создание обратной связи (доступно всем авторизованным)
    - update/partial_update: обновление обратной связи (только админы)
    - destroy: удаление обратной связи (только админы)
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Обычные пользователи видят только свою обратную связь
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        
        # Фильтрация по типу
        feedback_type = self.request.query_params.get('type', None)
        if feedback_type:
            queryset = queryset.filter(feedback_type=feedback_type)
        
        # Фильтрация по статусу
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.select_related('user')
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def resolve(self, request, pk=None):
        """
        Пометить обратную связь как решенную.
        POST /api/feedback/{id}/resolve/
        """
        from django.utils import timezone
        
        feedback = self.get_object()
        feedback.status = 'resolved'
        feedback.resolved_at = timezone.now()
        
        # Добавляем ответ администратора, если он указан
        admin_response = request.data.get('admin_response', '')
        if admin_response:
            feedback.admin_response = admin_response
        
        feedback.save()
        
        serializer = self.get_serializer(feedback)
        return Response(serializer.data)


class StatisticsView(APIView):
    """
    Предоставляет краткую статистику платформы.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        total_courses = Course.objects.count()
        total_lessons = Lesson.objects.count()
        total_students = User.objects.filter(role='student').count()
        total_teachers = User.objects.filter(role='teacher').count()

        return Response({
            'total_courses': total_courses,
            'total_lessons': total_lessons,
            'total_students': total_students,
            'total_teachers': total_teachers,
        })

