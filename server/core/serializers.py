from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обратной связи
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    screenshot_url = serializers.ImageField(source='screenshot', read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'user_name', 'user_email', 'feedback_type', 'title',
            'description', 'status', 'priority', 'screenshot', 'screenshot_url',
            'admin_response', 'created_at', 'updated_at', 'resolved_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'resolved_at']

    def create(self, validated_data):
        # Автоматически устанавливаем пользователя из запроса
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)