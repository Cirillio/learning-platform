# Руководство по сериализаторам Django REST Framework

## Обзор

В проекте Learning Platform используются сериализаторы Django REST Framework (DRF) для преобразования данных между Python-объектами и JSON. Сериализаторы обеспечивают валидацию, сериализацию и десериализацию данных для API.

## Структура сериализаторов

Сериализаторы организованы по приложениям Django:

### users/serializers.py

- `UserRegistrationSerializer` - Регистрация новых пользователей
- `UserProfileSerializer` - Управление профилями пользователей

### courses/serializers.py

- `CategorySerializer` - Категории курсов
- `CourseSerializer` - Базовый сериализатор курсов
- `CourseDetailSerializer` - Детальный просмотр курсов
- `LessonSerializer` - Базовый сериализатор уроков
- `LessonDetailSerializer` - Детальный просмотр уроков
- `LessonMaterialSerializer` - Материалы уроков
- `AssignmentSerializer` - Задания
- `AssignmentFileSerializer` - Файлы заданий
- `SubmissionSerializer` - Ответы на задания
- `SubmissionWithFilesSerializer` - Ответы с файлами
- `SubmissionFileSerializer` - Файлы ответов
- `GradeSerializer` - Оценки
- `CommentSerializer` - Комментарии

### core/serializers.py

- `FeedbackSerializer` - Обратная связь

### notifications/serializers.py

- `NotificationSerializer` - Уведомления

## Детальное описание

### UserRegistrationSerializer

**Назначение:** Регистрация новых пользователей с автоматическим созданием профиля.

**Особенности:**

- Валидация совпадения паролей
- Роле-специфичная валидация (специализация для преподавателей, студенческий билет для студентов)
- Автоматическое создание UserProfile

**Пример использования:**

```python
from users.serializers import UserRegistrationSerializer

serializer = UserRegistrationSerializer(data={
    'username': 'student1',
    'email': 'student@example.com',
    'password': 'securepass123',
    'password_confirm': 'securepass123',
    'role': 'student',
    'student_id': 'STU001',
    'enrollment_year': 2023
})

if serializer.is_valid():
    user = serializer.save()
```

### UserProfileSerializer

**Назначение:** Просмотр и редактирование профиля пользователя.

**Особенности:**

- Комбинирует поля User и UserProfile
- Некоторые поля User доступны только для чтения
- Поддержка роле-специфичных полей

**Пример использования:**

```python
from users.serializers import UserProfileSerializer

# Получение профиля
profile = user.profile
serializer = UserProfileSerializer(profile)
data = serializer.data

# Обновление профиля
serializer = UserProfileSerializer(profile, data=request.data, partial=True)
if serializer.is_valid():
    serializer.save()
```

### CourseSerializer и CourseDetailSerializer

**Назначение:** Сериализация курсов для списка и детального просмотра.

**Отличия:**

- `CourseSerializer`: базовая информация для списков
- `CourseDetailSerializer`: полная информация + статистика

**Вычисляемые поля:**

- `enrolled_count`: количество записанных студентов
- `lessons_count`: количество уроков
- `assignments_count`: общее количество заданий
- `is_enrolled`: статус записи текущего пользователя
- `progress`: прогресс обучения

**Пример использования:**

```python
from courses.serializers import CourseSerializer, CourseDetailSerializer

# Список курсов
courses = Course.objects.all()
serializer = CourseSerializer(courses, many=True)

# Детали курса
course = Course.objects.get(pk=1)
serializer = CourseDetailSerializer(course, context={'request': request})
```

### LessonSerializer и LessonDetailSerializer

**Назначение:** Сериализация уроков курса.

**Отличия:**

- `LessonSerializer`: базовая информация
- `LessonDetailSerializer`: + контент и материалы

**Вычисляемые поля:**

- `materials_count`: количество материалов
- `assignments_count`: количество заданий

### AssignmentSerializer

**Назначение:** Сериализация заданий для студентов.

**Вычисляемые поля:**

- `submissions_count`: количество отправленных решений
- `is_submitted`: отправил ли текущий студент решение

**Пример использования:**

```python
from courses.serializers import AssignmentSerializer

assignment = Assignment.objects.get(pk=1)
serializer = AssignmentSerializer(assignment, context={'request': request})
# serializer.data['is_submitted'] - True/False для текущего пользователя
```

### SubmissionSerializer и SubmissionWithFilesSerializer

**Назначение:** Сериализация ответов студентов на задания.

**Отличия:**

- `SubmissionSerializer`: базовая информация
- `SubmissionWithFilesSerializer`: + список файлов

**Вычисляемые поля:**

- `files_count`: количество прикрепленных файлов

### GradeSerializer

**Назначение:** Сериализация оценок за выполненные задания.

**Особенности:**

- Включает информацию о студенте, задании и преподавателе
- Только для чтения (оценки выставляются через API)

### CommentSerializer

**Назначение:** Сериализация комментариев к урокам и заданиям.

**Особенности:**

- Поддержка древовидной структуры (parent/replies)
- Generic relations для связи с разными объектами

**Вычисляемые поля:**

- `replies_count`: количество ответов
- `is_author`: является ли текущий пользователь автором

### FeedbackSerializer

**Назначение:** Сериализация обратной связи от пользователей.

**Особенности:**

- Автоматическая установка пользователя из запроса
- Поддержка типов: bug, feature, improvement, question, other
- Статусы: new, in_progress, resolved, closed

### NotificationSerializer

**Назначение:** Сериализация уведомлений пользователей.

**Особенности:**

- Generic relations для связи с любыми объектами
- Отслеживание статуса прочтения
- Интеграция с email-уведомлениями

## Общие паттерны использования

### Валидация данных

```python
serializer = SomeSerializer(data=request.data)
if serializer.is_valid():
    # Данные валидны
    obj = serializer.save()
else:
    # Обработка ошибок
    return Response(serializer.errors, status=400)
```

### Частичное обновление

```python
serializer = SomeSerializer(instance, data=request.data, partial=True)
```

### Контекст для вычисляемых полей

```python
serializer = SomeSerializer(data, context={'request': request})
```

### Работа с файлами

```python
# Сериализаторы автоматически обрабатывают FileField и ImageField
# URL доступен через *_url поля
serializer = FileSerializer(instance)
file_url = serializer.data['file_url']
```

## Связи между сериализаторами

- **Course** → **Lesson** (One-to-Many)
- **Lesson** → **LessonMaterial** (One-to-Many)
- **Lesson** → **Assignment** (One-to-Many)
- **Assignment** → **Submission** (One-to-Many)
- **Submission** → **SubmissionFile** (One-to-Many)
- **Submission** → **Grade** (One-to-One)
- **Assignment** → **AssignmentFile** (One-to-Many)
- **User** → **UserProfile** (One-to-One)
- **Generic relations** для Comment и Notification

## Лучшие практики

1. **Используйте context:** Передавайте `request` в context для полей, зависящих от пользователя
2. **Partial updates:** Используйте `partial=True` для PATCH запросов
3. **Валидация:** Всегда проверяйте `is_valid()` перед сохранением
4. **Read-only поля:** Помните о read_only_fields в Meta классе
5. **Generic relations:** Используйте для комментариев и уведомлений к разным объектам

## Тестирование сериализаторов

```python
from django.test import TestCase
from .serializers import UserRegistrationSerializer

class SerializerTestCase(TestCase):
    def test_user_registration_valid(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
            'role': 'student'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_user_registration_invalid_password(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'pass',
            'password_confirm': 'pass',
            'role': 'student'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
```

## Заключение

Сериализаторы обеспечивают надежный интерфейс между моделями Django и API. Правильное использование сериализаторов гарантирует валидность данных, безопасность и удобство разработки API.
