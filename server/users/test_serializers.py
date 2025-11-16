from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import UserProfile

User = get_user_model()


class UserRegistrationSerializerTest(TestCase):

    def test_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'a-very-strong-password-123!',
            'password_confirm': 'a-very-strong-password-123!',
            'first_name': 'Test',
            'last_name': 'User',
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password456',
            'first_name': 'Test',
            'last_name': 'User',
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_email_exists(self):
        User.objects.create_user(username='existinguser', email='test@example.com', password='password')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'a-very-strong-password-123!',
            'password_confirm': 'a-very-strong-password-123!',
            'first_name': 'Test',
            'last_name': 'User',
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


class UserProfileSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password')
        self.profile = UserProfile.objects.get(user=self.user)
        self.factory = APIRequestFactory()

    def test_read_only_fields(self):
        data = {
            'user': self.user.id,
            'student_id': 'new-student-id',
        }
        serializer = UserProfileSerializer(instance=self.profile, data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotEqual(serializer.validated_data.get('student_id'), 'new-student-id')

    def test_update_fields(self):
        data = {
            'bio': 'This is my new bio.',
            'phone': '1234567890',
        }
        serializer = UserProfileSerializer(instance=self.profile, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'This is my new bio.')
        self.assertEqual(self.profile.phone, '1234567890')
