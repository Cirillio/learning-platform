# Руководство по API Views

Это руководство описывает все созданные API ViewSets и endpoints для проекта.

## Структура API

### 1. Authentication (users app)

#### RegisterView

**Endpoint:** `POST /api/auth/register/`  
**Permissions:** AllowAny  
**Описание:** Регистрация нового пользователя

**Request Body:**

```json
{
  "username": "student1",
  "email": "student@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "role": "student",
  "first_name": "Иван",
  "last_name": "Иванов",
  "student_id": "ST-2024-001",
  "enrollment_year": 2024
}
```

**Response:**

```json
{
  "user": {
    "id": 1,
    "username": "student1",
    "email": "student@example.com",
    "role": "student"
  },
  "refresh": "refresh_token_here",
  "access": "access_token_here"
}
```

#### UserProfileView

**Endpoint:** `GET/PUT/PATCH /api/auth/profile/`  
**Permissions:** IsAuthenticated  
**Описание:** Получение и обновление профиля текущего пользователя

#### UserViewSet

**Endpoints:**

- `GET /api/users/` - список пользователей
- `GET /api/users/{id}/` - детали пользователя
- `GET /api/users/me/` - информация о текущем пользователе

**Permissions:** IsAuthenticated

---

### 2. Courses (courses app)

#### CategoryViewSet

**Endpoints:**

- `GET /api/categories/` - список категорий
- `GET /api/categories/{slug}/` - детали категории

**Permissions:** IsAuthenticatedOrReadOnly

#### CourseViewSet

**Endpoints:**

- `GET /api/courses/` - список курсов
- `POST /api/courses/` - создать курс (только преподаватели)
- `GET /api/courses/{slug}/` - детали курса
- `PUT/PATCH /api/courses/{slug}/` - обновить курс (только владелец)
- `DELETE /api/courses/{slug}/` - удалить курс (только владелец)

**Custom Actions:**

- `POST /api/courses/{slug}/enroll/` - записаться на курс (студенты)
- `POST /api/courses/{slug}/unenroll/` - отменить запись (студенты)
- `GET /api/courses/my_courses/` - мои курсы
- `GET /api/courses/{slug}/students/` - студенты курса (преподаватель)

**Query Parameters:**

- `category` - фильтр по категории (slug)
- `difficulty` - фильтр по сложности (beginner/intermediate/advanced)
- `status` - фильтр по статусу (draft/published/archived)
- `search` - поиск по названию/описанию

**Permissions:**

- list/retrieve: IsAuthenticatedOrReadOnly
- create: IsTeacher
- update/delete: IsCourseOwner

---

#### LessonViewSet

**Endpoints:**

- `GET /api/lessons/` - список уроков
- `POST /api/lessons/` - создать урок (преподаватели)
- `GET /api/lessons/{slug}/` - детали урока
- `PUT/PATCH /api/lessons/{slug}/` - обновить урок (преподаватели)
- `DELETE /api/lessons/{slug}/` - удалить урок (преподаватели)

**Query Parameters:**

- `course` - фильтр по курсу (slug)

**Permissions:**

- list/retrieve: IsAuthenticatedOrReadOnly
- create/update/delete: IsTeacher

---

#### AssignmentViewSet

**Endpoints:**

- `GET /api/assignments/` - список заданий
- `POST /api/assignments/` - создать задание (преподаватели)
- `GET /api/assignments/{id}/` - детали задания
- `PUT/PATCH /api/assignments/{id}/` - обновить задание (преподаватели)
- `DELETE /api/assignments/{id}/` - удалить задание (преподаватели)

**Query Parameters:**

- `lesson` - фильтр по уроку (id)
- `course` - фильтр по курсу (slug)

**Permissions:**

- list/retrieve: IsAuthenticatedOrReadOnly
- create/update/delete: IsTeacher

---

#### SubmissionViewSet

**Endpoints:**

- `GET /api/submissions/` - список ответов
- `POST /api/submissions/` - отправить ответ (студенты)
- `GET /api/submissions/{id}/` - детали ответа
- `PUT/PATCH /api/submissions/{id}/` - обновить ответ (автор)
- `DELETE /api/submissions/{id}/` - удалить ответ (автор)

**Query Parameters:**

- `assignment` - фильтр по заданию (id)

**Note:**

- Студенты видят только свои ответы
- Преподаватели видят все ответы
- Автоматическая проверка дедлайна при создании

**Permissions:**

- list/retrieve: IsAuthenticated
- create: IsStudent

---

#### GradeViewSet

**Endpoints:**

- `GET /api/grades/` - список оценок
- `POST /api/grades/` - выставить оценку (преподаватели)
- `GET /api/grades/{id}/` - детали оценки
- `PUT/PATCH /api/grades/{id}/` - обновить оценку (преподаватели)
- `DELETE /api/grades/{id}/` - удалить оценку (преподаватели)

**Query Parameters:**

- `submission` - фильтр по ответу (id)

**Note:**

- Студенты видят только свои оценки
- Автоматически обновляет статус ответа на "graded"

**Permissions:**

- list/retrieve: IsAuthenticated
- create/update/delete: IsTeacher

---

### 3. Comments & Feedback (core app)

#### CommentViewSet

**Endpoints:**

- `GET /api/comments/` - список комментариев
- `POST /api/comments/` - создать комментарий
- `GET /api/comments/{id}/` - детали комментария
- `PUT/PATCH /api/comments/{id}/` - обновить комментарий (автор)
- `DELETE /api/comments/{id}/` - удалить комментарий (автор)

**Query Parameters:**

- `content_type` - фильтр по типу контента (id)
- `object_id` - фильтр по ID объекта
- `parent` - фильтр по родительскому комментарию (id)
- `top_level=true` - только комментарии верхнего уровня

**Note:**

- Поддерживает древовидную структуру (replies)
- Generic relations для комментариев к разным объектам
- Автоматически устанавливает is_edited при обновлении

**Permissions:** IsAuthenticated

---

#### FeedbackViewSet

**Endpoints:**

- `GET /api/feedback/` - список обратной связи
- `POST /api/feedback/` - создать обратную связь
- `GET /api/feedback/{id}/` - детали обратной связи
- `PUT/PATCH /api/feedback/{id}/` - обновить (только админы)
- `DELETE /api/feedback/{id}/` - удалить (только админы)

**Custom Actions:**

- `POST /api/feedback/{id}/resolve/` - пометить как решенное (админы)

**Query Parameters:**

- `type` - фильтр по типу (bug/feature/improvement/question/other)
- `status` - фильтр по статусу (new/in_progress/resolved/closed)

**Note:**

- Обычные пользователи видят только свою обратную связь
- Админы видят всю обратную связь

**Permissions:**

- list/retrieve/create: IsAuthenticated
- update/delete: IsAdminUser

---

### 4. Notifications (notifications app)

#### NotificationViewSet

**Endpoints:**

- `GET /api/notifications/` - список уведомлений
- `GET /api/notifications/{id}/` - детали уведомления

**Custom Actions:**

- `POST /api/notifications/{id}/mark_as_read/` - пометить как прочитанное
- `POST /api/notifications/mark_all_as_read/` - пометить все как прочитанные
- `GET /api/notifications/unread_count/` - количество непрочитанных

**Query Parameters:**

- `is_read` - фильтр по статусу прочтения (true/false)
- `type` - фильтр по типу уведомления

**Note:**

- Пользователи видят только свои уведомления
- Автоматически устанавливает read_at при пометке как прочитанное

**Permissions:** IsAuthenticated

---

## Общие соглашения

### Пагинация

Все list endpoints поддерживают пагинацию (настраивается в settings.py):

```
GET /api/courses/?page=1&page_size=10
```

### Фильтрация и поиск

Используйте query parameters для фильтрации:

```
GET /api/courses/?category=programming&difficulty=beginner&search=python
```

### Сортировка

Некоторые endpoints поддерживают сортировку:

```
GET /api/courses/?ordering=-created_at
GET /api/courses/?ordering=title
```

### Permissions

- `AllowAny` - доступно всем
- `IsAuthenticated` - только авторизованным
- `IsTeacher` - только преподавателям
- `IsStudent` - только студентам
- `IsCourseOwner` - только владельцу курса
- `IsAdminUser` - только администраторам

### Ответы API

#### Успешный ответ (200, 201)

```json
{
  "data": {...}
}
```

#### Ошибка валидации (400)

```json
{
  "field_name": ["Описание ошибки"]
}
```

#### Ошибка авторизации (401)

```json
{
  "detail": "Учетные данные не были предоставлены."
}
```

#### Ошибка прав доступа (403)

```json
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

#### Объект не найден (404)

```json
{
  "detail": "Страница не найдена."
}
```

---

## Следующие шаги

После создания views необходимо:

1. ✅ Настроить URL routing (urls.py)
2. Протестировать все endpoints
3. Добавить документацию API (Swagger/ReDoc)
4. Написать unit тесты
