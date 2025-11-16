from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from .models import Category, Course, CourseEnrollment, Lesson, LessonMaterial, Assignment, Submission, Grade
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from django.urls import reverse


User = get_user_model()


class CategoryModelTest(TestCase):
    
    def test_create_category(self):
        """
        Проверяет создание категории и ее атрибуты.
        """
        category = Category.objects.create(
            name='Программирование',
            slug='programming'
        )
        self.assertEqual(category.name, 'Программирование')
        self.assertEqual(category.slug, 'programming')

    def test_category_str_representation(self):
        """
        Проверяет строковое представление модели Category.
        """
        category = Category.objects.create(name='Дизайн', slug='design')
        self.assertEqual(str(category), 'Дизайн')


class CourseModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='mainteacher',
            email='mainteacher@example.com',
            password='password123',
            role='teacher'
        )
        self.student1 = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='password123',
            role='student'
        )
        self.student2 = User.objects.create_user(
            username='student2',
            email='student2@example.com',
            password='password123',
            role='student'
        )
        self.category = Category.objects.create(name='Математика', slug='math')
        self.course = Course.objects.create(
            title='Введение в Алгебру',
            slug='intro-to-algebra',
            description='Курс для начинающих',
            short_description='Основы алгебры',
            teacher=self.teacher,
            category=self.category
        )

    def test_create_course(self):
        """
        Проверяет создание курса и его атрибуты.
        """
        self.assertEqual(self.course.title, 'Введение в Алгебру')
        self.assertEqual(self.course.teacher, self.teacher)
        self.assertEqual(self.course.status, 'draft')
        self.assertEqual(self.course.difficulty, 'beginner')

    def test_course_str_representation(self):
        """
        Проверяет строковое представление модели Course.
        """
        self.assertEqual(str(self.course), 'Введение в Алгебру')

    def test_course_teacher_must_have_teacher_role(self):
        """
        Проверяет, что курс может создать только пользователь с ролью 'teacher'.
        """
        course = Course(
            title='Неправильный курс',
            slug='invalid-course',
            description='Описание',
            short_description='Краткое описание',
            teacher=self.student1,
            category=self.category
        )
        with self.assertRaises(ValidationError):
            course.full_clean()

    def test_enrolled_count_property(self):
        """
        Проверяет, что свойство enrolled_count корректно считает студентов.
        """
        self.assertEqual(self.course.enrolled_count, 0)
        
        # Записываем одного студента
        CourseEnrollment.objects.create(student=self.student1, course=self.course)
        self.assertEqual(self.course.enrolled_count, 1)
        
        # Записываем второго студента
        CourseEnrollment.objects.create(student=self.student2, course=self.course)
        self.assertEqual(self.course.enrolled_count, 2)
        
        # Отчисляем одного студента
        enrollment = CourseEnrollment.objects.get(student=self.student1, course=self.course)
        enrollment.is_active = False
        enrollment.save()
        self.assertEqual(self.course.enrolled_count, 1)


class CourseEnrollmentModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', role='teacher', email='teacher@test.com', password='password')
        self.student = User.objects.create_user(
            username='student', role='student', email='student@test.com', password='password')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc')

    def test_enrollment_creation(self):
        enrollment = CourseEnrollment.objects.create(student=self.student, course=self.course)
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.course, self.course)
        self.assertTrue(enrollment.is_active)

    def test_enrollment_str_representation(self):
        enrollment = CourseEnrollment.objects.create(student=self.student, course=self.course)
        self.assertEqual(str(enrollment), 'student - Test Course')

    def test_unique_together_student_course(self):
        CourseEnrollment.objects.create(student=self.student, course=self.course)
        with self.assertRaises(IntegrityError):
            CourseEnrollment.objects.create(student=self.student, course=self.course)

    def test_enrollment_student_role_constraint(self):
        with self.assertRaises(ValidationError):
            enrollment = CourseEnrollment(student=self.teacher, course=self.course)
            enrollment.full_clean()


class LessonModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', role='teacher', email='teacher@test.com', password='password')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc')

    def test_lesson_creation(self):
        lesson = Lesson.objects.create(
            course=self.course, title='First Lesson', slug='first-lesson', content='Content')
        self.assertEqual(lesson.title, 'First Lesson')
        self.assertEqual(lesson.course, self.course)

    def test_lesson_str_representation(self):
        lesson = Lesson.objects.create(
            course=self.course, title='First Lesson', slug='first-lesson', content='Content')
        self.assertEqual(str(lesson), 'Test Course - First Lesson')

    def test_lesson_ordering(self):
        lesson1 = Lesson.objects.create(
            course=self.course, title='Lesson 1', slug='lesson-1', content='Content', order=1)
        lesson2 = Lesson.objects.create(
            course=self.course, title='Lesson 2', slug='lesson-2', content='Content', order=0)
        lessons = list(self.course.lessons.all())
        self.assertEqual(lessons, [lesson2, lesson1])

    def test_unique_together_course_slug(self):
        Lesson.objects.create(course=self.course, title='Lesson 1', slug='lesson-1', content='Content')
        with self.assertRaises(IntegrityError):
            Lesson.objects.create(course=self.course, title='Lesson 2', slug='lesson-1', content='Content')


class LessonMaterialModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', role='teacher', email='teacher@test.com', password='password')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc')
        self.lesson = Lesson.objects.create(
            course=self.course, title='First Lesson', slug='first-lesson', content='Content')
        self.file = SimpleUploadedFile("test_file.txt", b"file_content")

    def test_material_creation(self):
        material = LessonMaterial.objects.create(
            lesson=self.lesson, title='Test Material', file=self.file)
        self.assertEqual(material.title, 'Test Material')
        self.assertEqual(material.lesson, self.lesson)

    def test_material_str_representation(self):
        material = LessonMaterial.objects.create(
            lesson=self.lesson, title='Test Material', file=self.file)
        self.assertEqual(str(material), 'First Lesson - Test Material')

    def test_material_ordering(self):
        material1 = LessonMaterial.objects.create(
            lesson=self.lesson, title='Material 1', file=self.file, order=1)
        material2 = LessonMaterial.objects.create(
            lesson=self.lesson, title='Material 2', file=self.file, order=0)
        materials = list(self.lesson.materials.all())
        self.assertEqual(materials, [material2, material1])


class AssignmentModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', role='teacher', email='teacher@test.com', password='password')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc')
        self.lesson = Lesson.objects.create(
            course=self.course, title='First Lesson', slug='first-lesson', content='Content')

    def test_assignment_creation(self):
        assignment = Assignment.objects.create(
            lesson=self.lesson, title='First Assignment', description='Description', instructions='Instructions')
        self.assertEqual(assignment.title, 'First Assignment')
        self.assertEqual(assignment.lesson, self.lesson)

    def test_assignment_str_representation(self):
        assignment = Assignment.objects.create(
            lesson=self.lesson, title='First Assignment', description='Description', instructions='Instructions')
        self.assertEqual(str(assignment), 'First Lesson - First Assignment')


class SubmissionModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', role='teacher', email='teacher@test.com', password='password')
        self.student = User.objects.create_user(
            username='student', role='student', email='student@test.com', password='password')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc')
        self.lesson = Lesson.objects.create(
            course=self.course, title='First Lesson', slug='first-lesson', content='Content')
        self.assignment = Assignment.objects.create(
            lesson=self.lesson, title='First Assignment', description='Description', instructions='Instructions')

    def test_submission_creation(self):
        submission = Submission.objects.create(
            assignment=self.assignment, student=self.student, content='My submission')
        self.assertEqual(submission.assignment, self.assignment)
        self.assertEqual(submission.student, self.student)

    def test_submission_str_representation(self):
        submission = Submission.objects.create(
            assignment=self.assignment, student=self.student, content='My submission')
        self.assertEqual(str(submission), 'student - First Assignment')

    def test_unique_together_assignment_student(self):
        Submission.objects.create(
            assignment=self.assignment, student=self.student, content='My submission')
        with self.assertRaises(IntegrityError):
            Submission.objects.create(
                assignment=self.assignment, student=self.student, content='Another submission')

    def test_submission_student_role_constraint(self):
        with self.assertRaises(ValidationError):
            submission = Submission(
                assignment=self.assignment, student=self.teacher, content='My submission')
            submission.full_clean()


class GradeModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', role='teacher', email='teacher@test.com', password='password')
        self.student = User.objects.create_user(
            username='student', role='student', email='student@test.com', password='password')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc')
        self.lesson = Lesson.objects.create(
            course=self.course, title='First Lesson', slug='first-lesson', content='Content')
        self.assignment = Assignment.objects.create(
            lesson=self.lesson, title='First Assignment', description='Description', instructions='Instructions')
        self.submission = Submission.objects.create(
            assignment=self.assignment, student=self.student, content='My submission')

    def test_grade_creation(self):
        grade = Grade.objects.create(
            submission=self.submission, score=90, graded_by=self.teacher)
        self.assertEqual(grade.submission, self.submission)
        self.assertEqual(grade.score, 90)

    def test_grade_str_representation(self):
        grade = Grade.objects.create(
            submission=self.submission, score=90, graded_by=self.teacher)
        self.assertEqual(str(grade), 'student - First Assignment - 90')

    def test_one_to_one_grade_submission(self):
        Grade.objects.create(
            submission=self.submission, score=90, graded_by=self.teacher)
        with self.assertRaises(IntegrityError):
            Grade.objects.create(
                submission=self.submission, score=80, graded_by=self.teacher)

    def test_grade_teacher_role_constraint(self):
        with self.assertRaises(ValidationError):
            grade = Grade(submission=self.submission, score=90, graded_by=self.student)
            grade.full_clean()


class CourseAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            username='teacher', email='teacher@test.com', password='password', role='teacher')
        self.student = User.objects.create_user(
            username='student', email='student@test.com', password='password', role='student')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.course = Course.objects.create(
            title='Test Course', slug='test-course', teacher=self.teacher, description='desc', short_description='short desc', category=self.category)
        self.course_data = {
            'title': 'New Course',
            'slug': 'new-course',
            'description': 'A new course',
            'short_description': 'A new course',
            'category': self.category.id,
        }

    def test_list_courses(self):
        url = reverse('courses:course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_course(self):
        url = reverse('courses:course-detail', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Course')

    def test_create_course_by_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('courses:course-list')
        response = self.client.post(url, self.course_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Course.objects.count(), 2)

    def test_create_course_by_student(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('courses:course-list')
        response = self.client.post(url, self.course_data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_update_course_by_owner(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('courses:course-detail', kwargs={'slug': self.course.slug})
        data = {'title': 'Updated Course Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Course Title')

    def test_delete_course_by_owner(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('courses:course-detail', kwargs={'slug': self.course.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Course.objects.count(), 0)
