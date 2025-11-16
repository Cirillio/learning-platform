from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Comment, Feedback, ActivityLog
from courses.models import Course, Lesson

User = get_user_model()


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password')
        self.teacher = User.objects.create_user(
            username='teacher', email='teacher@example.com', password='password', role='teacher')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc')
        self.lesson = Lesson.objects.create(
            course=self.course, title='Test Lesson', slug='test-lesson', content='content')

    def test_comment_creation(self):
        comment = Comment.objects.create(
            content_object=self.lesson, author=self.user, text='Test comment')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.text, 'Test comment')
        self.assertEqual(comment.content_object, self.lesson)

    def test_comment_str_representation(self):
        comment = Comment.objects.create(
            content_object=self.lesson, author=self.user, text='This is a test comment that is longer than 50 characters to test truncation.')
        self.assertEqual(str(comment), 'testuser: This is a test comment that is longer than 50 char')

    def test_generic_foreign_key(self):
        comment = Comment.objects.create(
            content_object=self.lesson, author=self.user, text='Test comment')
        self.assertEqual(comment.content_type, ContentType.objects.get_for_model(Lesson))
        self.assertEqual(comment.object_id, self.lesson.id)

    def test_parent_child_relationship(self):
        parent_comment = Comment.objects.create(
            content_object=self.lesson, author=self.user, text='Parent comment')
        child_comment = Comment.objects.create(
            content_object=self.lesson, author=self.user, text='Child comment', parent=parent_comment)
        self.assertEqual(child_comment.parent, parent_comment)
        self.assertIn(child_comment, parent_comment.replies.all())


class FeedbackModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password')

    def test_feedback_creation(self):
        feedback = Feedback.objects.create(
            user=self.user, feedback_type='bug', title='Test Bug', description='A bug occurred')
        self.assertEqual(feedback.user, self.user)
        self.assertEqual(feedback.feedback_type, 'bug')
        self.assertEqual(feedback.status, 'new')

    def test_feedback_str_representation(self):
        feedback = Feedback.objects.create(
            user=self.user, feedback_type='feature', title='New Feature Request', description='Please add this feature')
        self.assertEqual(str(feedback), 'Новая функция: New Feature Request')


class ActivityLogModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password')
        self.teacher = User.objects.create_user(
            username='teacher', email='teacher@example.com', password='password', role='teacher')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc')

    def test_activity_log_creation(self):
        log = ActivityLog.objects.create(
            user=self.user, action='login', description='User logged in')
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action, 'login')

    def test_activity_log_str_representation(self):
        log = ActivityLog.objects.create(user=self.user, action='logout')
        self.assertTrue(str(log).startswith('testuser - Выход из системы - '))

    def test_generic_foreign_key(self):
        log = ActivityLog.objects.create(
            user=self.user, action='course_view', content_object=self.course)
        self.assertEqual(log.content_object, self.course)
        self.assertEqual(log.content_type, ContentType.objects.get_for_model(Course))
        self.assertEqual(log.object_id, self.course.id)
