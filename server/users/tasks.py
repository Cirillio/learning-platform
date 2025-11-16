"""
Celery tasks для users приложения.
"""
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

logger = logging.getLogger(__name__)

User = get_user_model()


@shared_task
def send_login_notification_email(user_id, ip_address, user_agent):
    """
    Отправить email-уведомление о входе в аккаунт.
    """
    logger.info(f"Starting login notification task for user {user_id}")
    
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"Found user {user.username}, email: {user.email}")
        
        if user.email:
            clean_email = user.email.strip().replace('\n', '').replace('\r', '')
            
            subject = 'Вход в ваш аккаунт'
            message = f'''Здравствуйте, {user.get_full_name() or user.username}!

            Мы зафиксировали новый вход в ваш аккаунт на нашем портале.

            Дата и время: {timezone.now().strftime("%d.%m.%Y %H:%M:%S")}
            IP-адрес: {ip_address or 'не определен'}
            User-Agent: {user_agent or 'не определен'}

            Если это были не вы, пожалуйста, немедленно смените пароль и свяжитесь с поддержкой.

            С уважением,
            Команда вашего учебного портала'''
            
            logger.info(f"Sending email to {clean_email}")

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[clean_email],
                fail_silently=False,
            )
            
            logger.info(f"Login notification sent to {clean_email}")
            return f'Login notification sent to {clean_email}'
        
        logger.warning(f'User {user_id} has no email.')
        return f'User {user_id} has no email.'
        
    except User.DoesNotExist:
        logger.error(f'User with id {user_id} not found.')
        return f'User with id {user_id} not found.'
    except Exception as e:
        logger.error(f'Error sending login notification: {str(e)}')
        return f'Error sending login notification: {str(e)}'