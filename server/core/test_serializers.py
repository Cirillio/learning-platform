from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from core.models import Comment, Feedback, ActivityLog
from core.serializers import CommentSerializer, FeedbackSerializer, ActivityLogSerializer
from courses.models import Lesson, Course
from users.serializers import BasicUserSerializer
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class CommentSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password')
        self.teacher = User.objects.create_user(
            username='teacher', email='teacher@example.com', password='password', role='teacher')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc')
        self.lesson = Lesson.objects.create(
            course=self.course, title='Test Lesson', slug='test-lesson', content='content')
        self.comment_data = {
            'content_type': ContentType.objects.get_for_model(self.lesson).id,
            'object_id': self.lesson.id,
            'text': 'This is a test comment.',
        }

    def test_valid_data(self):
        serializer = CommentSerializer(data=self.comment_data)
        if not serializer.is_valid():
            print("CommentSerializer errors:", serializer.errors)
        self.assertTrue(serializer.is_valid())

    def test_read_only_fields(self):
        comment = Comment.objects.create(
            content_object=self.lesson, author=self.user, text='Original comment')
        data = {
            'created_at': '2024-01-01T00:00:00Z',
            'is_edited': True,
        }
        serializer = CommentSerializer(instance=comment, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('created_at', serializer.validated_data)
        self.assertIn('is_edited', serializer.validated_data)

    def test_nested_data(self):
        comment = Comment.objects.create(
            content_object=self.lesson, author=self.user, text='Test comment')
        serializer = CommentSerializer(instance=comment)
        self.assertIn('author', serializer.data)
        self.assertEqual(serializer.data['author']['username'], self.user.username)


class FeedbackSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password')
        self.feedback_data = {
            'user': self.user.id,
            'feedback_type': 'bug',
            'title': 'Bug Report',
            'description': 'Found a bug.',
        }

    def test_valid_data(self):
        serializer = FeedbackSerializer(data=self.feedback_data)
        self.assertTrue(serializer.is_valid())

    def test_read_only_fields(self):
        feedback = Feedback.objects.create(
            user=self.user, feedback_type='bug', title='Bug', description='Desc')
        data = {
            'created_at': '2024-01-01T00:00:00Z',
            'status': 'resolved',
        }
        serializer = FeedbackSerializer(instance=feedback, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('created_at', serializer.validated_data)
        self.assertIn('status', serializer.validated_data)


class ActivityLogSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password')
        self.activity_log_data = {
            'user': self.user.id,
            'action': 'login',
            'description': 'User logged in.',
        }

    def test_valid_data(self):
        serializer = ActivityLogSerializer(data=self.activity_log_data)
        self.assertTrue(serializer.is_valid())

    def test_read_only_fields(self):
        log = ActivityLog.objects.create(
            user=self.user, action='logout', description='User logged out')
        data = {
            'created_at': '2024-01-01T00:00:00Z',
            'ip_address': '127.0.0.1',
        }
        serializer = ActivityLogSerializer(instance=log, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('created_at', serializer.validated_data)
        self.assertIn('ip_address', serializer.validated_data)

    def test_nested_data(self):
        log = ActivityLog.objects.create(
            user=self.user, action='login', description='User logged in.')
        serializer = ActivityLogSerializer(instance=log)
        self.assertIn('user', serializer.data)
        self.assertEqual(serializer.data['user']['username'], self.user.username)
