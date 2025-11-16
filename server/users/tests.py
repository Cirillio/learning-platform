from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserProfile
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()


class UserModelTest(TestCase):
    
    def test_create_user_default_role_is_student(self):
        """
        Проверяет, что у нового пользователя по умолчанию роль 'student'.
        """
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.assertEqual(user.role, 'student')
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_teacher)

    def test_create_teacher_user(self):
        """
        Проверяет создание пользователя с ролью 'teacher'.
        """
        teacher = User.objects.create_user(
            username='teacheruser',
            email='teacher@example.com',
            password='password123',
            role='teacher'
        )
        self.assertEqual(teacher.role, 'teacher')
        self.assertTrue(teacher.is_teacher)
        self.assertFalse(teacher.is_student)

    def test_user_str_representation(self):
        """
        Проверяет строковое представление модели User.
        """
        user = User.objects.create_user(username='testuser', email='test@example.com')
        self.assertEqual(str(user), "testuser (Student)")
        
        teacher = User.objects.create_user(username='teacheruser', email='teacher@example.com', role='teacher')
        self.assertEqual(str(teacher), "teacheruser (Teacher)")

    def test_email_is_unique(self):
        """
        Проверяет, что поле email является уникальным.
        """
        User.objects.create_user(username='user1', email='test@example.com', password='password')
        with self.assertRaises(Exception):
            User.objects.create_user(username='user2', email='test@example.com', password='password')


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password123',
            role='student'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='password123',
            role='teacher'
        )

    def test_profile_is_created_on_user_creation(self):
        """
        Проверяет, что профиль создается автоматически при создании пользователя.
        """
        self.assertTrue(hasattr(self.student_user, 'profile'))
        self.assertIsInstance(self.student_user.profile, UserProfile)
        self.assertEqual(UserProfile.objects.count(), 2)

    def test_profile_str_representation(self):
        """
        Проверяет строковое представление модели UserProfile.
        """
        self.assertEqual(str(self.student_user.profile), "Профиль student")
        self.assertEqual(str(self.teacher_user.profile), "Профиль teacher")

    def test_unique_student_id_is_generated_for_student(self):
        """
        Проверяет, что для студента генерируется уникальный student_id.
        """
        profile = self.student_user.profile
        self.assertIsNotNone(profile.student_id)
        self.assertTrue(profile.student_id.startswith('STUDENT-'))

    def test_student_id_is_not_generated_for_teacher(self):
        """
        Проверяет, что для преподавателя не генерируется student_id.
        """
        profile = self.teacher_user.profile
        self.assertTrue(profile.student_id is None or profile.student_id == '')


class UserAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'a-very-strong-password-123!',
            'password_confirm': 'a-very-strong-password-123!',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_user_registration(self):
        """
        Проверяет, что новый пользователь может быть создан.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_registration_with_existing_email(self):
        """
        Проверяет, что пользователь не может быть создан с существующим email.
        """
        User.objects.create_user(username='existinguser', email='test@example.com', password='password')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        """
        Проверяет, что пользователь может войти с правильными учетными данными.
        """
        User.objects.create_user(
            username='testuser', email='test@example.com', password='a-very-strong-password-123!')
        login_data = {'username': 'testuser', 'password': 'a-very-strong-password-123!'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.data)

    def test_user_login_with_incorrect_credentials(self):
        """
        Проверяет, что пользователь не может войти с неправильными учетными данными.
        """
        User.objects.create_user(
            username='testuser', email='test@example.com', password='a-very-strong-password-123!')
        login_data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, 401)
