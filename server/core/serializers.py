"""
Сериализаторы для приложения core.

Содержит сериализаторы для общих моделей:
- Комментарии (CommentSerializer)
- Обратная связь от пользователей (FeedbackSerializer)
"""

from rest_framework import serializers
from .models import Comment, Feedback


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев.

    Комментарии к урокам и заданиям. Поддерживает древовидную структуру (replies).

    Дополнительные поля:
    - author_name: имя автора комментария
    - author_avatar: аватар автора
    - replies_count: количество ответов на комментарий
    - is_author: является ли текущий пользователь автором
    """
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_avatar = serializers.ImageField(source='author.profile.avatar', read_only=True)
    replies_count = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'content_type', 'object_id', 'author', 'author_name', 'author_avatar',
            'text', 'parent', 'replies_count', 'is_author',
            'created_at', 'updated_at', 'is_edited'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at', 'is_edited']

    def get_replies_count(self, obj):
        return obj.replies.count()

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.author


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обратной связи от пользователей.

    Обратная связь может быть разных типов: баг, новая функция, улучшение, вопрос и т.д.
    Поддерживает прикрепление скриншотов и ответы администратора.

    Особенности:
    - Автоматически устанавливает пользователя из запроса
    - Поддерживает статусы: new, in_progress, resolved, closed
    - screenshot_url: URL прикрепленного скриншота
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