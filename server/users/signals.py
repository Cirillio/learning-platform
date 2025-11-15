import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Автоматически создает или обновляет профиль пользователя.
    При создании профиля для студента, если student_id не указан,
    генерирует уникальный номер.
    """
    if created:
        profile = UserProfile.objects.create(user=instance)
        # Если создан студент и у него нет студенческого билета
        if instance.role == 'student' and not profile.student_id:
            # Генерируем уникальный ID, например: STUDENT-123-A4B9C1
            profile.student_id = f"STUDENT-{instance.pk}-{uuid.uuid4().hex[:6].upper()}"
            profile.save()
    else:
        # Для существующих пользователей просто сохраняем профиль, если он есть
        if hasattr(instance, 'profile'):
            instance.profile.save()
