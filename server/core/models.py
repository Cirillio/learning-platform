from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    """
    Комментарии к урокам и заданиям
    """
    # Generic relation для комментариев к разным объектам
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Тип контента'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='ID объекта'
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Родительский комментарий'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    is_edited = models.BooleanField(
        default=False,
        verbose_name='Отредактирован'
    )
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.author.username}: {self.text[:50]}"


class Feedback(models.Model):
    """
    Обратная связь от пользователей
    """
    FEEDBACK_TYPES = (
        ('bug', 'Баг'),
        ('feature', 'Новая функция'),
        ('improvement', 'Улучшение'),
        ('question', 'Вопрос'),
        ('other', 'Другое'),
    )
    
    STATUS_CHOICES = (
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решено'),
        ('closed', 'Закрыто'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Пользователь'
    )
    feedback_type = models.CharField(
        max_length=20,
        choices=FEEDBACK_TYPES,
        verbose_name='Тип обратной связи'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    priority = models.PositiveIntegerField(
        default=3,
        verbose_name='Приоритет (1-5)'
    )
    screenshot = models.ImageField(
        upload_to='feedback_screenshots/',
        null=True,
        blank=True,
        verbose_name='Скриншот'
    )
    admin_response = models.TextField(
        blank=True,
        verbose_name='Ответ администратора'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата решения'
    )
    
    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_feedback_type_display()}: {self.title}"


class ActivityLog(models.Model):
    """
    Журнал активности пользователей
    """
    ACTION_TYPES = (
        ('login', 'Вход в систему'),
        ('logout', 'Выход из системы'),
        ('course_view', 'Просмотр курса'),
        ('lesson_view', 'Просмотр урока'),
        ('assignment_submit', 'Отправка задания'),
        ('assignment_grade', 'Оценка задания'),
        ('comment_create', 'Создание комментария'),
        ('enrollment', 'Запись на курс'),
        ('course_complete', 'Завершение курса'),
        ('other', 'Другое'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_logs',
        verbose_name='Пользователь'
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_TYPES,
        verbose_name='Действие'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP адрес'
    )
    user_agent = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='User Agent'
    )
    
    # Generic relation для связи с разными объектами
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Тип контента'
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='ID объекта'
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Запись журнала активности'
        verbose_name_plural = 'Журнал активности'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.created_at}"

