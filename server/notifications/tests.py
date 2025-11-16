from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from courses.models import Course

User = get_user_model()


class NotificationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='password123',
            role='teacher'
        )
        self.course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            description='A test course',
            short_description='A test course'
        )

    def test_notification_creation(self):
        """
        Проверяет создание уведомления и его атрибуты.
        """
        notification = Notification.objects.create(
            recipient=self.user,
            notification_type='new_lesson',
            title='Новый урок',
            message='В курсе появился новый урок.'
        )
        self.assertEqual(notification.recipient, self.user)
        self.assertEqual(notification.notification_type, 'new_lesson')
        self.assertFalse(notification.is_read)

    def test_notification_str_representation(self):
        """
        Проверяет строковое представление модели Notification.
        """
        notification = Notification.objects.create(
            recipient=self.user,
            title='Тестовое уведомление',
            message='Тест'
        )
        self.assertEqual(str(notification), 'testuser - Тестовое уведомление')

    def test_mark_as_read_method(self):
        """
        Проверяет, что метод mark_as_read корректно помечает уведомление как прочитанное.
        """
        notification = Notification.objects.create(
            recipient=self.user,
            title='Тест',
            message='Тест'
        )
        self.assertFalse(notification.is_read)
        self.assertIsNone(notification.read_at)
        
        notification.mark_as_read()
        notification.refresh_from_db()
        
        self.assertTrue(notification.is_read)
        self.assertIsNotNone(notification.read_at)

    def test_generic_foreign_key(self):
        """
        Проверяет работу GenericForeignKey с объектом Course.
        """
        notification = Notification.objects.create(
            recipient=self.user,
            title='Обновление курса',
            message='Курс был обновлен.',
            content_object=self.course
        )
        self.assertEqual(notification.content_object, self.course)
        self.assertEqual(notification.content_type, ContentType.objects.get_for_model(Course))
        self.assertEqual(notification.object_id, self.course.id)
