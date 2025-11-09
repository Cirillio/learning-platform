# Django Models - Документация

## Созданные модели

### 1. Users App (`users/`)

#### User (Кастомная модель пользователя)

- Расширяет `AbstractUser`
- Роли: `student` и `teacher`
- Дополнительные поля: `role`, уникальный `email`
- Методы: `is_teacher`, `is_student`

#### UserProfile

- Связь 1-к-1 с User
- Поля для преподавателей: `specialization`, `experience_years`
- Поля для студентов: `student_id`, `enrollment_year`
- Общие поля: `avatar`, `bio`, `phone`, `birth_date`, `address`, `city`, `country`

### 2. Courses App (`courses/`)

#### Category

- Категории курсов
- Поля: `name`, `slug`, `description`, `icon`

#### Course

- Основная модель курса
- Статусы: `draft`, `published`, `archived`
- Уровни сложности: `beginner`, `intermediate`, `advanced`
- Связи: `teacher` (User), `category` (Category)
- Поля: `title`, `slug`, `description`, `cover_image`, `status`, `difficulty`, `duration_weeks`, `max_students`, `is_featured`

#### CourseEnrollment

- Запись студента на курс
- Уникальная связь: `student` + `course`
- Отслеживание прогресса: `progress` (0-100%)
- Поля: `enrolled_at`, `is_active`, `completed_at`

#### Lesson

- Уроки в курсе
- Связь с `Course`
- Поля: `title`, `slug`, `content`, `description`, `order`, `duration_minutes`, `is_published`, `video_url`
- Уникальная связка: `course` + `slug`

#### LessonMaterial

- Материалы урока (файлы)
- Типы файлов: `pdf`, `doc`, `video`, `image`, `other`
- Поля: `lesson`, `title`, `file`, `file_type`, `file_size`, `order`

#### Assignment

- Задания для студентов
- Связь с `Lesson`
- Поля: `title`, `description`, `instructions`, `max_score`, `due_date`, `is_required`, `allow_late_submission`

#### AssignmentFile

- Файлы, прикрепленные к заданию преподавателем
- Поля: `assignment`, `file`, `filename`, `file_size`

#### Submission

- Ответ студента на задание
- Статусы: `pending`, `graded`, `returned`
- Уникальная связка: `assignment` + `student`
- Поля: `content`, `status`, `is_late`

#### SubmissionFile

- Файлы, прикрепленные студентом к ответу
- Поля: `submission`, `file`, `filename`, `file_size`

#### Grade

- Оценка за задание
- Связь 1-к-1 с `Submission`
- Поля: `score`, `feedback`, `graded_by` (Teacher), `graded_at`

### 3. Core App (`core/`)

#### Comment

- Комментарии к урокам и заданиям
- Generic Foreign Key для связи с любыми объектами
- Поддержка вложенности через `parent`
- Поля: `author`, `text`, `is_edited`

#### Feedback

- Обратная связь от пользователей
- Типы: `bug`, `feature`, `improvement`, `question`, `other`
- Статусы: `new`, `in_progress`, `resolved`, `closed`
- Поля: `user`, `feedback_type`, `title`, `description`, `status`, `priority`, `screenshot`, `admin_response`

#### ActivityLog

- Журнал активности пользователей
- Действия: `login`, `logout`, `course_view`, `lesson_view`, `assignment_submit`, `assignment_grade`, `comment_create`, `enrollment`, `course_complete`
- Generic Foreign Key для связи с объектами
- Поля: `user`, `action`, `description`, `ip_address`, `user_agent`

### 4. Notifications App (`notifications/`)

#### Notification

- Уведомления для пользователей
- Типы: `new_assignment`, `assignment_graded`, `assignment_deadline`, `new_comment`, `course_update`, `new_lesson`, `enrollment_approved`, `course_completed`, `system`
- Generic Foreign Key для связи с объектами
- Поля: `recipient`, `notification_type`, `title`, `message`, `is_read`, `read_at`, `email_sent`, `email_sent_at`
- Метод: `mark_as_read()`

## Django Admin

Все модели зарегистрированы в админ-панели с:

- `list_display` - отображаемые поля в списке
- `list_filter` - фильтры
- `search_fields` - поля для поиска
- `readonly_fields` - поля только для чтения
- Inline редактирование для связанных моделей
- Пользовательские действия (для Notification)

## Миграции

Все миграции созданы и применены:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Настройки (settings.py)

Добавлено:

```python
AUTH_USER_MODEL = 'users.User'
```

Приложения в `INSTALLED_APPS`:

- `users`
- `courses`
- `core`
- `notifications`

## Следующие шаги

1. ✅ Создать модели
2. ✅ Применить миграции
3. ✅ Зарегистрировать в admin
4. 🔜 Создать сериализаторы (DRF)
5. 🔜 Создать ViewSets и API endpoints
6. 🔜 Настроить permissions
7. 🔜 Создать URL роутинг
