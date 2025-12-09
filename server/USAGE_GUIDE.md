# Быстрый старт с моделями

## Создание суперпользователя

Для доступа к Django Admin создайте суперпользователя:

```bash
cd /home/cirillio/web/javascript/NUXT/University/server
/home/cirillio/web/javascript/NUXT/University/server/virtenv/bin/python manage.py createsuperuser
```

Введите:

- Username
- Email
- Password (дважды)

## Запуск сервера разработки

```bash
cd /home/cirillio/web/javascript/NUXT/University/server
/home/cirillio/web/javascript/NUXT/University/server/virtenv/bin/python manage.py runserver
```

Затем откройте в браузере:

- Django Admin: http://127.0.0.1:8000/admin/
- API (когда будет готово): http://127.0.0.1:8000/api/

## Структура моделей

### Пользователи

- **User**: Кастомная модель с ролями (student/teacher)
- **UserProfile**: Дополнительная информация о пользователе

### Курсы

- **Category**: Категории курсов
- **Course**: Курсы
- **CourseEnrollment**: Записи студентов на курсы
- **Lesson**: Уроки в курсе
- **LessonMaterial**: Материалы урока

### Задания

- **Assignment**: Задания для студентов
- **AssignmentFile**: Файлы задания от преподавателя
- **Submission**: Ответы студентов
- **SubmissionFile**: Файлы ответа студента
- **Grade**: Оценки за задания

### Взаимодействие

- **Comment**: Комментарии (к урокам, заданиям и т.д.)
- **Notification**: Уведомления пользователей
- **Feedback**: Обратная связь
- **ActivityLog**: Журнал активности

## Примеры использования в shell

```bash
python manage.py shell
```

### Создание преподавателя

```python
from users.models import User, UserProfile

teacher = User.objects.create_user(
    username='teacher1',
    email='teacher@example.com',
    password='password123',
    role='teacher',
    first_name='Иван',
    last_name='Преподавателев'
)

# Профиль создается автоматически через signals (если настроены)
# или вручную:
profile = UserProfile.objects.create(
    user=teacher,
    specialization='Web Development',
    experience_years=5
)
```

### Создание студента

```python
student = User.objects.create_user(
    username='student1',
    email='student@example.com',
    password='password123',
    role='student',
    first_name='Петр',
    last_name='Студентов'
)

profile = UserProfile.objects.create(
    user=student,
    student_id='STU001',
    enrollment_year=2024
)
```

### Создание курса

```python
from courses.models import Category, Course

category = Category.objects.create(
    name='Programming',
    slug='programming',
    description='Курсы по программированию'
)

course = Course.objects.create(
    title='Python для начинающих',
    slug='python-beginners',
    description='Полный курс Python',
    short_description='Изучите Python с нуля',
    teacher=teacher,
    category=category,
    status='published',
    difficulty='beginner',
    duration_weeks=8
)
```

### Запись студента на курс

```python
from courses.models import CourseEnrollment

enrollment = CourseEnrollment.objects.create(
    student=student,
    course=course,
    is_active=True
)
```

### Создание урока

```python
from courses.models import Lesson

lesson = Lesson.objects.create(
    course=course,
    title='Введение в Python',
    slug='introduction-to-python',
    description='Первый урок',
    content='# Добро пожаловать в Python\n\nПython - это...',
    order=1,
    is_published=True,
    duration_minutes=45
)
```

### Создание задания

```python
from courses.models import Assignment
from datetime import datetime, timedelta

assignment = Assignment.objects.create(
    lesson=lesson,
    title='Первая программа',
    description='Напишите программу Hello World',
    instructions='1. Создайте файл hello.py\n2. Напишите print("Hello World")',
    max_score=100,
    due_date=datetime.now() + timedelta(days=7),
    is_required=True
)
```

### Отправка ответа студентом

```python
from courses.models import Submission

submission = Submission.objects.create(
    assignment=assignment,
    student=student,
    content='print("Hello World")',
    status='pending'
)
```

### Оценка работы

```python
from courses.models import Grade

grade = Grade.objects.create(
    submission=submission,
    score=95,
    feedback='Отличная работа! Небольшое замечание: можно было добавить комментарий.',
    graded_by=teacher
)

# Обновляем статус submission
submission.status = 'graded'
submission.save()
```

### Создание комментария

```python
from core.models import Comment
from django.contrib.contenttypes.models import ContentType

# Комментарий к уроку
comment = Comment.objects.create(
    content_type=ContentType.objects.get_for_model(lesson),
    object_id=lesson.id,
    author=student,
    text='Отличный урок, все понятно!'
)
```

### Создание уведомления

```python
from notifications.models import Notification

notification = Notification.objects.create(
    recipient=student,
    notification_type='assignment_graded',
    title='Ваша работа оценена',
    message=f'Преподаватель оценил вашу работу "{assignment.title}". Оценка: {grade.score}/{assignment.max_score}',
    content_type=ContentType.objects.get_for_model(grade),
    object_id=grade.id
)
```

## Полезные команды

### Просмотр всех курсов

```python
from courses.models import Course
courses = Course.objects.filter(status='published')
for course in courses:
    print(f"{course.title} - {course.teacher.username}")
```

### Получение всех уроков курса

```python
lessons = course.lessons.filter(is_published=True).order_by('order')
```

### Проверка прогресса студента

```python
enrollments = student.course_enrollments.filter(is_active=True)
for enrollment in enrollments:
    print(f"{enrollment.course.title}: {enrollment.progress}%")
```

### Получение непрочитанных уведомлений

```python
unread_notifications = student.notifications.filter(is_read=False)
print(f"Непрочитанных уведомлений: {unread_notifications.count()}")
```

## Полезные querysets

```python
# Все опубликованные курсы преподавателя
teacher.courses_teaching.filter(status='published')

# Все активные записи студента
student.course_enrollments.filter(is_active=True)

# Все задания урока
lesson.assignments.all()

# Все ответы студента с оценкой
student.submissions.filter(status='graded')

# Последние 10 событий в журнале активности
from core.models import ActivityLog
ActivityLog.objects.filter(user=student).order_by('-created_at')[:10]
```

## Очистка базы данных (для разработки)

**ВНИМАНИЕ: Это удалит все данные!**

```bash
cd /home/cirillio/web/javascript/NUXT/University/server
rm db.sqlite3
rm -rf */migrations/00*.py
/home/cirillio/web/javascript/NUXT/University/server/virtenv/bin/python manage.py makemigrations
/home/cirillio/web/javascript/NUXT/University/server/virtenv/bin/python manage.py migrate
/home/cirillio/web/javascript/NUXT/University/server/virtenv/bin/python manage.py createsuperuser
```
