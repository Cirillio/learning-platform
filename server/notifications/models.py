from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    """
    Уведомления для пользователей
    """
    NOTIFICATION_TYPES = (
        ('new_assignment', 'Новое задание'),
        ('assignment_graded', 'Задание оценено'),
        ('assignment_deadline', 'Срок сдачи задания'),
        ('new_comment', 'Новый комментарий'),
        ('course_update', 'Обновление курса'),
        ('new_lesson', 'Новый урок'),
        ('enrollment_approved', 'Запись на курс одобрена'),
        ('course_completed', 'Курс завершен'),
        ('system', 'Системное уведомление'),
        ('other', 'Другое'),
    )
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Получатель'
    )
    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES,
        verbose_name='Тип уведомления'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    message = models.TextField(
        verbose_name='Сообщение'
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
    
    is_read = models.BooleanField(
        default=False,
        verbose_name='Прочитано'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата прочтения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    # Дополнительные поля для email уведомлений
    email_sent = models.BooleanField(
        default=False,
        verbose_name='Email отправлен'
    )
    email_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата отправки email'
    )
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.recipient.username} - {self.title}"
    
    def mark_as_read(self):
        """Пометить уведомление как прочитанное"""
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

