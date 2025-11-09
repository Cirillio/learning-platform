from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import User, UserProfile
from courses.models import Category, Course, CourseEnrollment, Lesson, Assignment, Submission, Grade
from notifications.models import Notification
from core.models import Comment, Feedback


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Начинаем заполнение базы данных...'))

        # Создаем преподавателей
        teacher1 = self.create_teacher('teacher1', 'teacher1@example.com', 'Иван', 'Иванов', 'Web Development', 5)
        teacher2 = self.create_teacher('teacher2', 'teacher2@example.com', 'Мария', 'Петрова', 'Data Science', 8)
        
        # Создаем студентов
        student1 = self.create_student('student1', 'student1@example.com', 'Петр', 'Сидоров', 'STU001', 2024)
        student2 = self.create_student('student2', 'student2@example.com', 'Анна', 'Смирнова', 'STU002', 2024)
        student3 = self.create_student('student3', 'student3@example.com', 'Алексей', 'Козлов', 'STU003', 2023)
        
        # Создаем категории
        cat_programming = Category.objects.create(
            name='Программирование',
            slug='programming',
            description='Курсы по программированию',
            icon='code'
        )
        
        cat_data_science = Category.objects.create(
            name='Data Science',
            slug='data-science',
            description='Курсы по анализу данных',
            icon='chart'
        )
        
        # Создаем курсы
        course1 = Course.objects.create(
            title='Python для начинающих',
            slug='python-beginners',
            description='Полный курс Python с нуля до профессионала',
            short_description='Изучите Python с нуля за 8 недель',
            teacher=teacher1,
            category=cat_programming,
            status='published',
            difficulty='beginner',
            duration_weeks=8,
            max_students=30,
            is_featured=True
        )
        
        course2 = Course.objects.create(
            title='Django Web Framework',
            slug='django-web-framework',
            description='Создание веб-приложений на Django',
            short_description='Научитесь создавать профессиональные веб-приложения',
            teacher=teacher1,
            category=cat_programming,
            status='published',
            difficulty='intermediate',
            duration_weeks=10,
            max_students=25,
            is_featured=True
        )
        
        course3 = Course.objects.create(
            title='Введение в Data Science',
            slug='intro-data-science',
            description='Основы анализа данных и машинного обучения',
            short_description='Начните карьеру в Data Science',
            teacher=teacher2,
            category=cat_data_science,
            status='published',
            difficulty='beginner',
            duration_weeks=12,
            max_students=20
        )
        
        # Записываем студентов на курсы
        CourseEnrollment.objects.create(student=student1, course=course1, is_active=True, progress=45)
        CourseEnrollment.objects.create(student=student1, course=course2, is_active=True, progress=20)
        CourseEnrollment.objects.create(student=student2, course=course1, is_active=True, progress=60)
        CourseEnrollment.objects.create(student=student3, course=course3, is_active=True, progress=75)
        
        # Создаем уроки для course1
        lesson1 = Lesson.objects.create(
            course=course1,
            title='Введение в Python',
            slug='introduction-to-python',
            description='Первое знакомство с Python',
            content='# Добро пожаловать в мир Python!\n\nPython - это мощный и простой язык программирования...',
            order=1,
            is_published=True,
            duration_minutes=45,
            video_url='https://youtube.com/watch?v=example1'
        )
        
        lesson2 = Lesson.objects.create(
            course=course1,
            title='Переменные и типы данных',
            slug='variables-and-data-types',
            description='Основные типы данных в Python',
            content='# Переменные и типы данных\n\nВ Python есть несколько базовых типов данных...',
            order=2,
            is_published=True,
            duration_minutes=60,
            video_url='https://youtube.com/watch?v=example2'
        )
        
        lesson3 = Lesson.objects.create(
            course=course1,
            title='Условные конструкции',
            slug='conditional-statements',
            description='If, elif, else в Python',
            content='# Условные конструкции\n\nУсловные конструкции позволяют выполнять код в зависимости от условий...',
            order=3,
            is_published=True,
            duration_minutes=50
        )
        
        # Создаем задания
        assignment1 = Assignment.objects.create(
            lesson=lesson1,
            title='Hello World',
            description='Напишите первую программу',
            instructions='1. Создайте файл hello.py\n2. Напишите программу, которая выводит "Hello World"',
            max_score=100,
            due_date=timezone.now() + timedelta(days=7),
            is_required=True,
            allow_late_submission=True
        )
        
        assignment2 = Assignment.objects.create(
            lesson=lesson2,
            title='Работа с переменными',
            description='Создайте переменные разных типов',
            instructions='1. Создайте переменные для имени, возраста, роста\n2. Выведите их значения',
            max_score=100,
            due_date=timezone.now() + timedelta(days=10),
            is_required=True
        )
        
        # Создаем ответы студентов
        submission1 = Submission.objects.create(
            assignment=assignment1,
            student=student1,
            content='print("Hello World")',
            status='graded',
            is_late=False
        )
        
        submission2 = Submission.objects.create(
            assignment=assignment1,
            student=student2,
            content='# Моя первая программа\nprint("Hello World")\nprint("Привет, мир!")',
            status='graded',
            is_late=False
        )
        
        # Создаем оценки
        Grade.objects.create(
            submission=submission1,
            score=90,
            feedback='Хорошая работа! В следующий раз добавьте комментарии.',
            graded_by=teacher1
        )
        
        Grade.objects.create(
            submission=submission2,
            score=100,
            feedback='Отлично! Программа работает идеально, комментарии на месте.',
            graded_by=teacher1
        )
        
        # Создаем комментарии
        from django.contrib.contenttypes.models import ContentType
        
        Comment.objects.create(
            content_type=ContentType.objects.get_for_model(lesson1),
            object_id=lesson1.id,
            author=student1,
            text='Отличный урок! Все очень понятно объяснено.'
        )
        
        Comment.objects.create(
            content_type=ContentType.objects.get_for_model(lesson1),
            object_id=lesson1.id,
            author=student2,
            text='Спасибо за урок! Очень помогло разобраться с основами.'
        )
        
        # Создаем уведомления
        Notification.objects.create(
            recipient=student1,
            notification_type='assignment_graded',
            title='Ваша работа оценена',
            message='Преподаватель оценил вашу работу "Hello World". Оценка: 90/100',
            content_type=ContentType.objects.get_for_model(submission1),
            object_id=submission1.id,
            is_read=False
        )
        
        Notification.objects.create(
            recipient=student2,
            notification_type='assignment_graded',
            title='Ваша работа оценена',
            message='Преподаватель оценил вашу работу "Hello World". Оценка: 100/100',
            content_type=ContentType.objects.get_for_model(submission2),
            object_id=submission2.id,
            is_read=True
        )
        
        Notification.objects.create(
            recipient=student1,
            notification_type='new_assignment',
            title='Новое задание',
            message='Преподаватель добавил новое задание "Работа с переменными"',
            content_type=ContentType.objects.get_for_model(assignment2),
            object_id=assignment2.id,
            is_read=False
        )
        
        # Создаем обратную связь
        Feedback.objects.create(
            user=student1,
            feedback_type='feature',
            title='Добавить мобильное приложение',
            description='Было бы здорово иметь мобильное приложение для изучения курсов',
            status='new',
            priority=3
        )
        
        Feedback.objects.create(
            user=student2,
            feedback_type='improvement',
            title='Улучшить поиск по курсам',
            description='Добавить фильтры по уровню сложности и категориям',
            status='in_progress',
            priority=4
        )
        
        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
        self.stdout.write(self.style.SUCCESS(f'Создано:'))
        self.stdout.write(f'  - Преподавателей: 2')
        self.stdout.write(f'  - Студентов: 3')
        self.stdout.write(f'  - Категорий: 2')
        self.stdout.write(f'  - Курсов: 3')
        self.stdout.write(f'  - Уроков: 3')
        self.stdout.write(f'  - Заданий: 2')
        self.stdout.write(f'  - Ответов: 2')
        self.stdout.write(f'  - Оценок: 2')
        self.stdout.write(f'  - Комментариев: 2')
        self.stdout.write(f'  - Уведомлений: 3')
        self.stdout.write(f'  - Обратной связи: 2')

    def create_teacher(self, username, email, first_name, last_name, specialization, experience):
        """Создает преподавателя с профилем"""
        user = User.objects.create_user(
            username=username,
            email=email,
            password='password123',
            role='teacher',
            first_name=first_name,
            last_name=last_name
        )
        
        profile = user.profile
        profile.specialization = specialization
        profile.experience_years = experience
        profile.bio = f'Опытный преподаватель в области {specialization}'
        profile.save()
        
        self.stdout.write(f'  Создан преподаватель: {username}')
        return user

    def create_student(self, username, email, first_name, last_name, student_id, enrollment_year):
        """Создает студента с профилем"""
        user = User.objects.create_user(
            username=username,
            email=email,
            password='password123',
            role='student',
            first_name=first_name,
            last_name=last_name
        )
        
        profile = user.profile
        profile.student_id = student_id
        profile.enrollment_year = enrollment_year
        profile.bio = f'Студент, поступивший в {enrollment_year} году'
        profile.save()
        
        self.stdout.write(f'  Создан студент: {username}')
        return user
