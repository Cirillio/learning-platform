from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уведомлений
    """
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'notification_type', 'title', 'message',
            'content_type', 'object_id', 'is_read', 'read_at',
            'created_at', 'email_sent', 'email_sent_at'
        ]
        read_only_fields = [
            'recipient', 'read_at', 'created_at', 'email_sent', 'email_sent_at'
        ]