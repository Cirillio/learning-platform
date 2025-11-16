"""
Celery configuration for the project.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Устанавливаем переменную окружения для Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем экземпляр Celery
app = Celery('university')

# Загружаем конфигурацию из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим tasks в приложениях
app.autodiscover_tasks()

# Настройка периодических задач (Celery Beat)
app.conf.beat_schedule = {
    'check-assignment-deadlines': {
        'task': 'courses.tasks.check_assignment_deadlines',
        'schedule': crontab(hour='*/1'),  # Каждый час
    },
    'send-pending-notifications': {
        'task': 'notifications.tasks.send_pending_email_notifications',
        'schedule': crontab(minute='*/15'),  # Каждые 15 минут
    },
    'clear-blacklisted-tokens': {
        'task': 'users.tasks.clear_blacklisted_tokens',
        'schedule': crontab(hour=0, minute=0),  # Каждый день в полночь
    },
}

@app.task(bind=True)
def debug_task(self):
    """Отладочная задача для тестирования Celery"""
    print(f'Request: {self.request!r}')
