"""
Celery tasks для notifications приложения.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Notification


@shared_task
def send_pending_email_notifications():
    """
    Периодическая задача для отправки email уведомлений.
    Отправляет email для непрочитанных уведомлений, которым еще не отправлен email.
    """
    # Получаем уведомления без отправленного email
    notifications = Notification.objects.filter(
        email_sent=False,
        is_read=False
    ).select_related('recipient')[:50]  # Ограничиваем 50 за раз
    
    count = 0
    for notification in notifications:
        if notification.recipient.email:
            try:
                send_mail(
                    subject=notification.title,
                    message=notification.message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[notification.recipient.email],
                    fail_silently=False,
                )
                
                # Помечаем как отправленное
                notification.email_sent = True
                notification.email_sent_at = timezone.now()
                notification.save(update_fields=['email_sent', 'email_sent_at'])
                count += 1
            except Exception as e:
                print(f'Error sending email for notification {notification.id}: {str(e)}')
    
    return f'Sent {count} email notifications'


@shared_task
def send_notification_email(notification_id):
    """
    Отправить email для конкретного уведомления.
    """
    try:
        notification = Notification.objects.select_related('recipient').get(id=notification_id)
        
        if notification.recipient.email and not notification.email_sent:
            send_mail(
                subject=notification.title,
                message=notification.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.recipient.email],
                fail_silently=False,
            )
            
            notification.email_sent = True
            notification.email_sent_at = timezone.now()
            notification.save(update_fields=['email_sent', 'email_sent_at'])
            
            return f'Email sent for notification {notification_id}'
        
        return f'Email not sent for notification {notification_id}'
    except Notification.DoesNotExist:
        return f'Notification {notification_id} not found'
    except Exception as e:
        return f'Error: {str(e)}'


@shared_task
def cleanup_old_notifications():
    """
    Периодическая задача для очистки старых прочитанных уведомлений.
    Удаляет прочитанные уведомления старше 30 дней.
    """
    from datetime import timedelta
    
    threshold_date = timezone.now() - timedelta(days=30)
    
    deleted_count, _ = Notification.objects.filter(
        is_read=True,
        read_at__lt=threshold_date
    ).delete()
    
    return f'Deleted {deleted_count} old notifications'
