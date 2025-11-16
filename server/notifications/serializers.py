"""
Сериализаторы для приложения notifications.

Содержит сериализаторы для:
- Уведомлений пользователей (NotificationSerializer)
"""

from rest_framework import serializers
from .models import Notification
from users.serializers import BasicUserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уведомлений пользователей.

    Уведомления могут быть разных типов: новые задания, оцененные работы,
    комментарии, обновления курсов и т.д.

    Особенности:
    - Поддерживает generic relations для связи с разными объектами
    - Автоматически устанавливает получателя
    - Отслеживает статус прочтения и отправки email
    """
    recipient = BasicUserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'notification_type', 'title', 'message',
            'content_type', 'object_id', 'is_read', 'read_at',
            'created_at', 'email_sent', 'email_sent_at'
        ]
        read_only_fields = [
            'read_at', 'created_at', 'email_sent', 'email_sent_at'
        ]