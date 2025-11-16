from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from users.serializers import BasicUserSerializer

User = get_user_model()


class NotificationSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password')
        self.notification_data = {
            'recipient': self.user.id,
            'notification_type': 'system',
            'title': 'Test Notification',
            'message': 'This is a test message.',
        }

    def test_valid_data(self):
        serializer = NotificationSerializer(data=self.notification_data)
        self.assertTrue(serializer.is_valid())

    def test_read_only_fields(self):
        notification = Notification.objects.create(**self.notification_data)
        data = {
            'created_at': '2024-01-01T00:00:00Z',
            'is_read': True,
        }
        serializer = NotificationSerializer(instance=notification, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('created_at', serializer.validated_data)
        self.assertIn('is_read', serializer.validated_data) # is_read is not read-only

    def test_nested_data(self):
        notification = Notification.objects.create(**self.notification_data)
        serializer = NotificationSerializer(instance=notification)
        self.assertIn('recipient', serializer.data)
        self.assertEqual(serializer.data['recipient']['username'], self.user.username)
