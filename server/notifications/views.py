from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для уведомлений.
    
    - list: список уведомлений текущего пользователя
    - retrieve: детали уведомления
    
    Дополнительные actions:
    - mark_as_read: пометить уведомление как прочитанное
    - mark_all_as_read: пометить все уведомления как прочитанные
    - unread_count: количество непрочитанных уведомлений
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Пользователи видят только свои уведомления
        queryset = Notification.objects.filter(recipient=self.request.user)
        
        # Фильтрация по статусу прочтения
        is_read = self.request.query_params.get('is_read', None)
        if is_read is not None:
            is_read = is_read.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(is_read=is_read)
        
        # Фильтрация по типу уведомления
        notification_type = self.request.query_params.get('type', None)
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        return queryset.select_related('content_type')
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Пометить уведомление как прочитанное.
        POST /api/notifications/{id}/mark_as_read/
        """
        notification = self.get_object()
        notification.mark_as_read()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Пометить все уведомления как прочитанные.
        POST /api/notifications/mark_all_as_read/
        """
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({
            'detail': f'Помечено {count} уведомлений как прочитанные.'
        })
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Получить количество непрочитанных уведомлений.
        GET /api/notifications/unread_count/
        """
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        
        return Response({'count': count})

