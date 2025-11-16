from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from courses.models import Category, Course
from courses.serializers import CourseSerializer, CourseDetailSerializer

User = get_user_model()


class CourseSerializerTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', email='teacher@test.com', password='password', role='teacher')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.course_data = {
            'title': 'New Course',
            'slug': 'new-course',
            'description': 'A new course',
            'short_description': 'A new course',
            'teacher': self.teacher.id,
            'category': self.category.id,
        }

    def test_valid_data(self):
        serializer = CourseSerializer(data=self.course_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_missing_fields(self):
        invalid_data = self.course_data.copy()
        invalid_data.pop('title')
        serializer = CourseSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)


class CourseDetailSerializerTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', email='teacher@test.com', password='password', role='teacher')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc', category=self.category)

    def test_read_only_fields(self):
        serializer = CourseDetailSerializer(instance=self.course)
        self.assertIn('created_at', serializer.data)
        self.assertIn('updated_at', serializer.data)
        # Attempt to update a read-only field
        data = {'created_at': '2024-01-01T00:00:00Z'}
        serializer = CourseDetailSerializer(instance=self.course, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('created_at', serializer.validated_data)

    def test_nested_data(self):
        serializer = CourseDetailSerializer(instance=self.course)
        self.assertIn('teacher', serializer.data)
        self.assertIn('category', serializer.data)
        self.assertEqual(serializer.data['teacher']['username'], self.teacher.username)
        self.assertEqual(serializer.data['category']['name'], self.category.name)
