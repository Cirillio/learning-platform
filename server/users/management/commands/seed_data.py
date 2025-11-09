from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import User, UserProfile
from courses.models import Category, Course, CourseEnrollment, Lesson, Assignment, Submission, Grade
from notifications.models import Notification
from core.models import Comment, Feedback
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными для полноценного тестирования'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Начинаем расширенное заполнение базы данных...'))

        # --- БАЗОВЫЕ СУЩНОСТИ ---
        self.stdout.write(self.style.SUCCESS('\nСоздание базовых сущностей...'))
        
        teacher1 = self.create_teacher('teacher1', 'teacher1@example.com', 'Иван', 'Иванов', 'Web Development', 5)
        teacher2 = self.create_teacher('teacher2', 'teacher2@example.com', 'Мария', 'Петрова', 'Data Science', 8)
        
        student1 = self.create_student('student1', 'student1@example.com', 'Петр', 'Сидоров', 'STU001', 2024)
        student2 = self.create_student('student2', 'student2@example.com', 'Анна', 'Смирнова', 'STU002', 2024)
        student3 = self.create_student('student3', 'student3@example.com', 'Алексей', 'Козлов', 'STU003', 2023)
        
        cat_programming, _ = Category.objects.get_or_create(slug='programming', defaults={'name':'Программирование', 'description':'Курсы по программированию', 'icon':'code'})
        cat_data_science, _ = Category.objects.get_or_create(slug='data-science', defaults={'name':'Data Science', 'description':'Курсы по анализу данных', 'icon':'chart'})
        
        course1, _ = Course.objects.get_or_create(
            slug='python-beginners',
            defaults={
                'title':'Python для начинающих', 'description':'Полный курс Python с нуля до профессионала',
                'short_description':'Изучите Python с нуля за 8 недель', 'teacher':teacher1, 'category':cat_programming,
                'status':'published', 'difficulty':'beginner', 'duration_weeks':8, 'max_students':30, 'is_featured':True
            }
        )
        
        course2, _ = Course.objects.get_or_create(
            slug='django-web-framework',
            defaults={
                'title':'Django Web Framework', 'description':'Создание веб-приложений на Django',
                'short_description':'Научитесь создавать профессиональные веб-приложения', 'teacher':teacher1, 'category':cat_programming,
                'status':'published', 'difficulty':'intermediate', 'duration_weeks':10, 'max_students':25, 'is_featured':True
            }
        )
        
        course3, _ = Course.objects.get_or_create(
            slug='intro-data-science',
            defaults={
                'title':'Введение в Data Science', 'description':'Основы анализа данных и машинного обучения',
                'short_description':'Начните карьеру в Data Science', 'teacher':teacher2, 'category':cat_data_science,
                'status':'published', 'difficulty':'beginner', 'duration_weeks':12, 'max_students':20
            }
        )
        
        CourseEnrollment.objects.get_or_create(student=student1, course=course1, defaults={'is_active':True, 'progress':45})
        CourseEnrollment.objects.get_or_create(student=student1, course=course2, defaults={'is_active':True, 'progress':20})
        CourseEnrollment.objects.get_or_create(student=student2, course=course1, defaults={'is_active':True, 'progress':60})
        CourseEnrollment.objects.get_or_create(student=student3, course=course3, defaults={'is_active':True, 'progress':75})
        CourseEnrollment.objects.get_or_create(student=student2, course=course2, defaults={'is_active':True, 'progress':30})
        CourseEnrollment.objects.get_or_create(student=student3, course=course1, defaults={'is_active':False, 'progress':10})
        
        lesson1, _ = Lesson.objects.get_or_create(course=course1, slug='introduction-to-python', defaults={'title':'Введение в Python', 'order':1, 'is_published':True})
        lesson2, _ = Lesson.objects.get_or_create(course=course1, slug='variables-and-data-types', defaults={'title':'Переменные и типы данных', 'order':2, 'is_published':True})
        lesson3, _ = Lesson.objects.get_or_create(course=course1, slug='conditional-statements', defaults={'title':'Условные конструкции', 'order':3, 'is_published':True})
        lesson4, _ = Lesson.objects.get_or_create(course=course2, slug='introduction-to-django', defaults={'title':'Введение в Django', 'order':1, 'is_published':True})
        lesson5, _ = Lesson.objects.get_or_create(course=course2, slug='models-and-database', defaults={'title':'Модели и база данных', 'order':2, 'is_published':True})
        lesson6, _ = Lesson.objects.get_or_create(course=course3, slug='intro-to-data-analysis', defaults={'title':'Введение в анализ данных', 'order':1, 'is_published':True})
        
        assignment1, _ = Assignment.objects.get_or_create(lesson=lesson1, title='Hello World', defaults={'max_score':100, 'due_date':timezone.now() + timedelta(days=7)})
        assignment2, _ = Assignment.objects.get_or_create(lesson=lesson2, title='Работа с переменными', defaults={'max_score':100, 'due_date':timezone.now() + timedelta(days=10)})
        
        submission1, _ = Submission.objects.get_or_create(assignment=assignment1, student=student1, defaults={'content':'print("Hello World")', 'status':'graded'})
        submission2, _ = Submission.objects.get_or_create(assignment=assignment1, student=student2, defaults={'content':'print("Hello World")', 'status':'graded'})
        
        Grade.objects.get_or_create(submission=submission1, defaults={'score':90, 'feedback':'Хорошая работа!', 'graded_by':teacher1})
        Grade.objects.get_or_create(submission=submission2, defaults={'score':100, 'feedback':'Отлично!', 'graded_by':teacher1})

        # --- РАСШИРЕННЫЕ СЦЕНАРИИ И ГРАНИЧНЫЕ СЛУЧАИ ---
        self.stdout.write(self.style.WARNING('\nСоздаем данные для граничных случаев и расширенного тестирования...'))

        teacher3 = self.create_teacher('teacher3', 'teacher3@example.com', 'Сергей', 'Николаев', 'UX/UI Design', 4)
        student4 = self.create_student('student4', 'student4@example.com', 'Ольга', 'Морозова', 'STU004', 2025)
        self.stdout.write(self.style.SUCCESS('  - Созданы: студент без курсов и преподаватель без курсов'))

        cat_design, _ = Category.objects.get_or_create(slug='design', defaults={'name':'Дизайн', 'description':'Курсы по дизайну и UX/UI', 'icon':'palette'})

        Course.objects.get_or_create(
            slug='ux-ui-design-basics',
            defaults={'title':'Основы UX/UI дизайна', 'teacher':teacher3, 'category':cat_design, 'status':'draft'}
        )
        self.stdout.write(self.style.SUCCESS('  - Создан курс в статусе "черновик"'))

        Course.objects.get_or_create(
            slug='empty-course',
            defaults={'title':'Пустой курс (для теста)', 'teacher':teacher1, 'category':cat_programming, 'status':'published'}
        )
        self.stdout.write(self.style.SUCCESS('  - Создан опубликованный курс без уроков'))

        course_full, _ = Course.objects.get_or_create(
            slug='advanced-javascript',
            defaults={
                'title':'Продвинутый JavaScript', 'teacher':teacher1, 'category':cat_programming,
                'status':'published', 'difficulty':'advanced', 'max_students':2
            }
        )
        CourseEnrollment.objects.get_or_create(student=student1, course=course_full, defaults={'is_active':True, 'progress':10})
        CourseEnrollment.objects.get_or_create(student=student2, course=course_full, defaults={'is_active':True, 'progress':5})
        CourseEnrollment.objects.get_or_create(student=student3, course=course_full, defaults={'is_active':False, 'progress':0})
        self.stdout.write(self.style.SUCCESS('  - Создан курс с заполненными местами'))

        assignment_past_due, _ = Assignment.objects.get_or_create(
            lesson=lesson2, title='Задание с прошедшим сроком',
            defaults={
                'description':'Это задание, срок которого уже прошел.', 'max_score':50,
                'due_date':timezone.now() - timedelta(days=2), 'allow_late_submission':True
            }
        )
        Submission.objects.get_or_create(
            assignment=assignment_past_due, student=student1,
            defaults={
                'content':'print("Это запоздалый ответ")', 'status':'submitted',
                'submitted_at':timezone.now() - timedelta(days=1), 'is_late':True
            }
        )
        self.stdout.write(self.style.SUCCESS('  - Создано задание с прошедшим сроком и запоздалый ответ'))

        course_pagination, _ = Course.objects.get_or_create(
            slug='pagination-test-course',
            defaults={
                'title':'Большой курс для пагинации', 'teacher':teacher2,
                'category':cat_data_science, 'status':'published', 'difficulty':'intermediate'
            }
        )
        if course_pagination.lessons.count() < 25:
            for i in range(course_pagination.lessons.count() + 1, 28):
                Lesson.objects.create(
                    course=course_pagination, title=f'Урок {i}: Основы чего-то там', slug=f'lesson-{i}-basics',
                    content=f'# Урок {i}\n\nЭто подробное содержание урока.', order=i, is_published=True
                )
        self.stdout.write(self.style.SUCCESS(f'  - Курс для пагинации теперь содержит {course_pagination.lessons.count()} уроков'))

        if student2.notifications.count() < 35:
            for i in range(student2.notifications.count() + 1, 36):
                Notification.objects.create(
                    recipient=student2, notification_type='info', title=f'Информационное уведомление #{i}',
                    message=f'Это уведомление номер {i} из большой пачки.', is_read=(i % 5 == 0)
                )
        self.stdout.write(self.style.SUCCESS(f'  - Пользователь для пагинации теперь имеет {student2.notifications.count()} уведомлений'))
        
        Feedback.objects.get_or_create(
            user=student4, title='Не могу найти кнопку',
            defaults={'feedback_type':'bug', 'description':'На странице профиля пропала кнопка редактирования.', 'status':'new', 'priority':5}
        )
        self.stdout.write(self.style.SUCCESS('  - Добавлены новые отзывы'))

        self.stdout.write(self.style.SUCCESS('\nБаза данных успешно заполнена расширенным набором данных!'))
        self.stdout.write(self.style.SUCCESS(f'Всего в базе данных:'))
        self.stdout.write(f'  - Преподавателей: {User.objects.filter(role="teacher").count()}')
        self.stdout.write(f'  - Студентов: {User.objects.filter(role="student").count()}')
        self.stdout.write(f'  - Категорий: {Category.objects.count()}')
        self.stdout.write(f'  - Курсов: {Course.objects.count()}')
        self.stdout.write(f'  - Записей на курсы: {CourseEnrollment.objects.count()}')
        self.stdout.write(f'  - Уроков: {Lesson.objects.count()}')
        self.stdout.write(f'  - Заданий: {Assignment.objects.count()}')
        self.stdout.write(f'  - Ответов: {Submission.objects.count()}')
        self.stdout.write(f'  - Оценок: {Grade.objects.count()}')
        self.stdout.write(f'  - Комментариев: {Comment.objects.count()}')
        self.stdout.write(f'  - Уведомлений: {Notification.objects.count()}')
        self.stdout.write(f'  - Обратной связи: {Feedback.objects.count()}')

    def create_teacher(self, username, email, first_name, last_name, specialization, experience):
        """Создает или обновляет преподавателя с профилем"""
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email, 'role': 'teacher', 'first_name': first_name, 'last_name': last_name
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(f'  Создан преподаватель: {username}')
        
        profile = user.profile
        profile.specialization = specialization
        profile.experience_years = experience
        profile.bio = f'Опытный преподаватель в области {specialization}'
        profile.save()
        
        return user

    def create_student(self, username, email, first_name, last_name, student_id, enrollment_year):
        """Создает или обновляет студента с профилем"""
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email, 'role': 'student', 'first_name': first_name, 'last_name': last_name
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(f'  Создан студент: {username}')
        
        profile = user.profile
        profile.student_id = student_id
        profile.enrollment_year = enrollment_year
        profile.bio = f'Студент, поступивший в {enrollment_year} году'
        profile.save()
        
        return user
