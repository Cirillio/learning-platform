# Руководство по Permissions Django REST Framework

## Обзор

Permissions в проекте Learning Platform контролируют доступ к API эндпоинтам на основе ролей пользователей и отношений владения. Все permissions наследуются от `BasePermission` DRF.

## Структура Permissions

Permissions организованы по приложениям:

### users/permissions.py
- `IsTeacher` - Проверка роли преподавателя
- `IsStudent` - Проверка роли студента

### courses/permissions.py
- `IsOwner` - Проверка владения объектом
- `IsCourseOwner` - Проверка владения курсом
- `IsTeacherOrReadOnly` - Преподаватели могут изменять, остальные только читать

## Детальное описание

### IsTeacher

**Назначение:** Разрешать доступ только преподавателям.

**Логика:**
```python
request.user.is_authenticated and request.user.role == 'teacher'
```

**Использование:**
- Создание и редактирование курсов
- Управление уроками и заданиями
- Выставление оценок

**Пример:**
```python
from users.permissions import IsTeacher

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
```

### IsStudent

**Назначение:** Разрешать доступ только студентам.

**Логика:**
```python
request.user.is_authenticated and request.user.role == 'student'
```

**Использование:**
- Отправка решений на задания
- Запись на курсы
- Просмотр личных оценок

### IsOwner

**Назначение:** Разрешать действия только владельцу объекта.

**Логика владения:**
- `Course`: `obj.teacher == request.user`
- `Lesson/Assignment/Grade`: `obj.course.teacher == request.user`
- `Comment`: `obj.author == request.user`
- `Submission`: `obj.student == request.user`

**Особенности:**
- Работает только на уровне объекта (`has_object_permission`)
- Используется для персонального контента

**Пример:**
```python
from courses.permissions import IsOwner

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
```

### IsCourseOwner

**Назначение:** Разрешать действия только преподавателю курса.

**Логика:**
- Для списков: преподаватели могут создавать, остальные читают
- Для объектов: только преподаватель курса может изменять

**Определение курса:**
- `obj.course` (для уроков)
- `obj.lesson.course` (для заданий)
- `obj.assignment.lesson.course` (для оценок)

**Использование:**
- Управление уроками курса
- Создание заданий
- Выставление оценок

### IsTeacherOrReadOnly

**Назначение:** Преподаватели имеют полный доступ, остальные - только чтение.

**Логика:**
- `SAFE_METHODS` (GET, HEAD, OPTIONS): все аутентифицированные пользователи
- `POST/PUT/DELETE`: только преподаватели

**Использование:**
- Категории курсов
- Общие материалы
- Публичные ресурсы

## Примеры использования в ViewSets

### Курсы (только преподаватели могут создавать)
```python
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrReadOnly]
```

### Задания (только владелец курса может управлять)
```python
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsCourseOwner]
```

### Комментарии (только автор может редактировать)
```python
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
```

### Ответы на задания (студенты могут отправлять, преподаватели просматривать)
```python
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsStudent()]
        return [IsAuthenticated(), IsCourseOwner()]
```

## Комбинирование Permissions

### Логические операторы
```python
from rest_framework.permissions import AND, OR

# Преподаватель ИЛИ владелец
permission_classes = [IsAuthenticated & (IsTeacher | IsOwner)]

# Преподаватель ИЛИ (студент И владелец)
permission_classes = [IsAuthenticated & (IsTeacher | (IsStudent & IsOwner))]
```

### Кастомные комбинации
```python
class IsTeacherOrOwner(BasePermission):
    def has_permission(self, request, view):
        return IsTeacher().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return (
            IsTeacher().has_object_permission(request, view, obj) or
            IsOwner().has_object_permission(request, view, obj)
        )
```

## Тестирование Permissions

```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from .permissions import IsTeacher

class PermissionTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.teacher = get_user_model().objects.create_user(
            username='teacher',
            role='teacher'
        )
        self.student = get_user_model().objects.create_user(
            username='student',
            role='student'
        )

    def test_is_teacher_permission(self):
        request = self.factory.get('/')
        request.user = self.teacher

        permission = IsTeacher()
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.student
        self.assertFalse(permission.has_permission(request, None))
```

## Лучшие практики

1. **Минимальные права:** Давайте минимально необходимые права
2. **Явные проверки:** Используйте `has_object_permission` для объектного уровня
3. **Ролевые модели:** Четко разделяйте логику по ролям
4. **Тестирование:** Проверяйте permissions в тестах
5. **Документация:** Описывайте логику permissions в docstrings

## Безопасность

- Всегда проверяйте аутентификацию перед авторизацией
- Используйте `has_object_permission` для чувствительных операций
- Не доверяйте клиентским данным для определения прав
- Логируйте подозрительные попытки доступа

## Заключение

Permissions обеспечивают безопасность API, контролируя доступ на основе ролей и владения. Правильное использование permissions критично для защиты данных и функциональности платформы.