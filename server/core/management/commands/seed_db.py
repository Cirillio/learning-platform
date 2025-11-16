
# Сохрани как: your_app/management/commands/seed_db.py
# Запуск: python manage.py seed_db

import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify

# Импортируй твои модели (замени your_app на имя твоего приложения)
from courses.models import (
    Category, Course, Lesson, Assignment,
    CourseEnrollment, Submission, Grade
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными для LMS'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед заполнением',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Очистка старых данных...')
            Grade.objects.all().delete()
            Submission.objects.all().delete()
            CourseEnrollment.objects.all().delete()
            Assignment.objects.all().delete()
            Lesson.objects.all().delete()
            Course.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Данные очищены'))

        # Получаем существующих пользователей
        teachers = list(User.objects.filter(role='teacher'))
        students = list(User.objects.filter(role='student'))

        if not teachers:
            self.stdout.write(self.style.ERROR('Нет учителей в БД! Создай хотя бы одного.'))
            return

        if not students:
            self.stdout.write(self.style.WARNING('Нет студентов в БД. Создам тестовых.'))
            students = self.create_students(5)

        # 1. Создаём категории
        self.stdout.write('Создание категорий...')
        categories = self.create_categories()
        self.stdout.write(self.style.SUCCESS(f'✓ Создано {len(categories)} категорий'))

        # 2. Создаём курсы
        self.stdout.write('Создание курсов...')
        courses = self.create_courses(categories, teachers)
        self.stdout.write(self.style.SUCCESS(f'✓ Создано {len(courses)} курсов'))

        # 3. Создаём уроки
        self.stdout.write('Создание уроков...')
        lessons = self.create_lessons(courses)
        self.stdout.write(self.style.SUCCESS(f'✓ Создано {len(lessons)} уроков'))

        # 4. Создаём задания
        self.stdout.write('Создание заданий...')
        assignments = self.create_assignments(lessons)
        self.stdout.write(self.style.SUCCESS(f'✓ Создано {len(assignments)} заданий'))

        # 5. Записываем студентов на курсы
        self.stdout.write('Запись студентов на курсы...')
        enrollments = self.enroll_students(courses, students)
        self.stdout.write(self.style.SUCCESS(f'✓ Создано {len(enrollments)} записей'))

        # 6. Создаём ответы и оценки
        self.stdout.write('Создание ответов и оценок...')
        submissions, grades = self.create_submissions_and_grades(assignments, students, teachers)
        self.stdout.write(self.style.SUCCESS(
            f'✓ Создано {len(submissions)} ответов и {len(grades)} оценок'
        ))

        self.stdout.write(self.style.SUCCESS('\n🎉 База данных успешно заполнена!'))
        self.print_summary(categories, courses, lessons, assignments, enrollments)

    def create_students(self, count):
        students = []
        for i in range(1, count + 1):
            student, created = User.objects.get_or_create(
                username=f'teststudent{i}',
                defaults={
                    'email': f'student{i}@test.com',
                    'password': 'testpass123',
                    'first_name': f'Тестовый',
                    'last_name': f'Студент{i}',
                    'role': 'student',
                }
            )
            if created:
                student.set_password('testpass123')
                student.save()
            students.append(student)
        return students

    def create_categories(self):
        category_data = [
            {'name': 'Программирование', 'slug': 'programming', 'description': 'Курсы по разработке ПО'},
            {'name': 'Веб-разработка', 'slug': 'web-dev', 'description': 'Frontend и Backend'},
            {'name': 'Data Science', 'slug': 'data-science', 'description': 'Анализ данных и ML'},
            {'name': 'Мобильная разработка', 'slug': 'mobile-dev', 'description': 'iOS и Android'},
            {'name': 'DevOps', 'slug': 'devops', 'description': 'CI/CD и инфраструктура'},
            {'name': 'Дизайн', 'slug': 'design', 'description': 'UI/UX дизайн'},
            {'name': 'Маркетинг', 'slug': 'marketing', 'description': 'Digital-маркетинг'},
            {'name': 'Бизнес', 'slug': 'business', 'description': 'Управление проектами'},
        ]

        categories = []
        for data in category_data:
            cat, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults={'name': data['name'], 'description': data['description']}
            )
            categories.append(cat)
        return categories

    def create_courses(self, categories, teachers):
        course_templates = [
            # Программирование
            ('Python для начинающих', 'Основы программирования на Python', 'programming', 'beginner'),
            ('Python: продвинутый уровень', 'ООП, декораторы, генераторы', 'programming', 'advanced'),
            ('JavaScript: основы', 'Изучаем JS с нуля', 'programming', 'beginner'),
            ('TypeScript для профи', 'Типизация и продвинутые паттерны', 'programming', 'advanced'),

            # Веб-разработка
            ('Django REST Framework', 'Создание REST API на Django', 'web-dev', 'intermediate'),
            ('Vue.js 3 + Composition API', 'Современный Vue', 'web-dev', 'intermediate'),
            ('Nuxt 3: Full-Stack', 'SSR и Universal приложения', 'web-dev', 'advanced'),
            ('HTML/CSS: с нуля до PRO', 'Вёрстка и адаптивность', 'web-dev', 'beginner'),

            # Data Science
            ('Pandas и NumPy', 'Анализ данных в Python', 'data-science', 'beginner'),
            ('Machine Learning: основы', 'Scikit-learn и теория', 'data-science', 'intermediate'),
            ('Deep Learning с PyTorch', 'Нейронные сети', 'data-science', 'advanced'),

            # Мобильная разработка
            ('Flutter для начинающих', 'Кросс-платформенные приложения', 'mobile-dev', 'beginner'),
            ('React Native: продвинутый', 'Нативные модули и оптимизация', 'mobile-dev', 'advanced'),

            # DevOps
            ('Docker и Kubernetes', 'Контейнеризация приложений', 'devops', 'intermediate'),
            ('CI/CD с GitHub Actions', 'Автоматизация деплоя', 'devops', 'intermediate'),

            # Дизайн
            ('Figma: UI/UX дизайн', 'Создание интерфейсов', 'design', 'beginner'),
            ('Дизайн-системы', 'Создание масштабируемого дизайна', 'design', 'advanced'),

            # Маркетинг и бизнес
            ('SMM с нуля', 'Продвижение в соцсетях', 'marketing', 'beginner'),
            ('Agile и Scrum', 'Управление проектами', 'business', 'intermediate'),
        ]

        courses = []
        for i, (title, short_desc, cat_slug, level) in enumerate(course_templates):
            category = next(c for c in categories if c.slug == cat_slug)
            teacher = random.choice(teachers)
            slug = slugify(title)

            course, created = Course.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': f'Полное описание курса "{title}". Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                    'short_description': short_desc,
                    'category': category,
                    'teacher': teacher,
                    'difficulty': level,
                    'duration_weeks': random.randint(4, 16),
                    'status': random.choice(['published', 'published', 'published', 'draft']),  # 75% опубликованы
                    'max_students': random.choice([None, 50, 100, 150]),
                    'is_featured': random.choice([True, False, False, False]),
                }
            )
            courses.append(course)

        return courses

    def create_lessons(self, courses):
        lessons = []

        for course in courses:
            num_lessons = random.randint(8, 20)

            for lesson_num in range(1, num_lessons + 1):
                lesson_titles = [
                    f'Урок {lesson_num}: Введение в {course.title}',
                    f'Урок {lesson_num}: Основные концепции',
                    f'Урок {lesson_num}: Практическое применение',
                    f'Урок {lesson_num}: Продвинутые техники',
                    f'Урок {lesson_num}: Разбор реальных кейсов',
                ]
                title = random.choice(lesson_titles)
                slug = slugify(f'{course.slug}-{title}')

                lesson, created = Lesson.objects.get_or_create(
                    course=course,
                    slug=slug,
                    defaults={
                        'title': title,
                        'description': f'Подробное объяснение материала урока {lesson_num}',
                        'content': f'''
# {title}

## Введение
Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Основной материал
- Пункт 1
- Пункт 2
- Пункт 3

## Практическое задание
Попробуйте применить изученное на практике.

## Дополнительные материалы
- Ссылка 1
- Ссылка 2
                        '''.strip(),
                        'duration_minutes': random.randint(15, 90),
                        'order': lesson_num,
                        'is_published': random.choice([True, True, True, False]),
                    }
                )
                lessons.append(lesson)

        return lessons

    def create_assignments(self, lessons):
        assignments = []

        # Создаём задания для ~40% уроков
        for lesson in random.sample(lessons, k=len(lessons) // 2):
            num_assignments = random.randint(1, 2)

            for assign_num in range(1, num_assignments + 1):
                due_date = timezone.now() + timedelta(days=random.randint(7, 30))

                assignment, created = Assignment.objects.get_or_create(
                    lesson=lesson,
                    title=f'Задание {assign_num}: {lesson.title}',
                    defaults={
                        'description': f'Описание задания {assign_num} для урока "{lesson.title}".',
                        'instructions': f'''
## Задание {assign_num}

Выполните следующие шаги:
1. Изучите материал урока
2. Решите практическую задачу
3. Загрузите результат

**Критерии оценки:**
- Правильность решения (50%)
- Качество кода (30%)
- Документация (20%)

Удачи!
                        '''.strip(),
                        'due_date': due_date,
                        'max_score': random.choice([10, 20, 50, 100]),
                        'is_required': random.choice([True, True, False]),
                        'allow_late_submission': random.choice([True, False]),
                    }
                )
                assignments.append(assignment)

        return assignments

    def enroll_students(self, courses, students):
        enrollments = []

        for student in students:
            # Каждый студент записывается на 3-7 курсов
            num_courses = random.randint(3, 7)
            student_courses = random.sample(courses, k=min(num_courses, len(courses)))

            for course in student_courses:
                enrollment, created = CourseEnrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'enrolled_at': timezone.now() - timedelta(days=random.randint(1, 60)),
                        'progress': random.randint(0, 100),
                    }
                )
                if created:
                    enrollments.append(enrollment)

        return enrollments

    def create_submissions_and_grades(self, assignments, students, teachers):
        submissions = []
        grades = []

        for assignment in assignments:
            # Получаем студентов, записанных на этот курс
            enrolled_students_ids = CourseEnrollment.objects.filter(
                course=assignment.lesson.course
            ).values_list('student_id', flat=True)

            course_students = [s for s in students if s.id in enrolled_students_ids]

            # 60-80% студентов сдают задание
            submitting_students = random.sample(
                course_students,
                k=random.randint(len(course_students) // 2, len(course_students))
            ) if course_students else []

            for student in submitting_students:
                submitted_at = timezone.now() - timedelta(days=random.randint(0, 10))
                is_late = assignment.due_date and submitted_at > assignment.due_date

                submission_status = random.choice(['pending', 'graded', 'returned'])

                submission, created = Submission.objects.get_or_create(
                    assignment=assignment,
                    student=student,
                    defaults={
                        'content': f'''
# Ответ на задание "{assignment.title}"

Решение задачи:

```python
def solution():
    return "Done!"
```

Объяснение: Lorem ipsum dolor sit amet.
                        '''.strip(),
                        'submitted_at': submitted_at,
                        'status': submission_status,
                        'is_late': is_late,
                    }
                )
                submissions.append(submission)

                # Создаём оценку для "оцененных" ответов
                if submission_status == 'graded':
                    score = random.randint(
                        int(assignment.max_score * 0.5),
                        assignment.max_score
                    )

                    grade, created = Grade.objects.get_or_create(
                        submission=submission,
                        defaults={
                            'score': score,
                            'graded_by': assignment.lesson.course.teacher,
                            'feedback': random.choice([
                                'Отличная работа!',
                                'Хорошо, но есть что улучшить',
                                'Есть ошибки, исправьте и отправьте снова',
                                'Молодец! Все правильно',
                            ]),
                            'graded_at': submitted_at + timedelta(days=random.randint(1, 5)),
                        }
                    )
                    grades.append(grade)

        return submissions, grades

    def print_summary(self, categories, courses, lessons, assignments, enrollments):
        self.stdout.write('\n' + '='*50)
        self.stdout.write('СВОДКА:')
        self.stdout.write(f'  Категорий: {len(categories)}')
        self.stdout.write(f'  Курсов: {len(courses)}')
        self.stdout.write(f'  Уроков: {len(lessons)}')
        self.stdout.write(f'  Заданий: {len(assignments)}')
        self.stdout.write(f'  Записей на курсы: {len(enrollments)}')
        self.stdout.write('='*50)
