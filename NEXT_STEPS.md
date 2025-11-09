# Следующие шаги реализации

## ✅ Выполнено

- [x] Docker Compose конфигурация (SQLite + Redis + Django + Nuxt + Nginx)
- [x] Dockerfile для Django backend
- [x] Dockerfile для Nuxt frontend
- [x] .env файлы (примеры)
- [x] requirements.txt для Python
- [x] .dockerignore файлы
- [x] Nginx конфигурация
- [x] .gitignore
- [x] README.md
- [x] Makefile с удобными командами

---

## 📋 Следующие этапы

### 1. Настройка окружения

- [x] Скопировать `.env.example` → `.env` для backend
- [x] Скопировать `.env.example` → `.env` для frontend
- [x] Сгенерировать SECRET_KEY для Django
- [x] Настроить ALLOWED_HOSTS при необходимости

### 2. Backend - Django Settings

- [x] Настроить `settings.py`:
  - [x] Подключить DRF
  - [x] Настроить JWT (simplejwt)
  - [x] Настроить CORS
  - [x] Настроить Celery
  - [x] Настроить пути для MEDIA и STATIC
  - [x] Добавить созданные приложения в INSTALLED_APPS

### 3. Backend - Модели

- [x] Создать кастомную модель User (с ролями teacher/student)
- [x] Создать модель UserProfile
- [x] Создать модель Course
- [x] Создать модель CourseEnrollment
- [x] Создать модель Category
- [x] Создать модель Lesson
- [x] Создать модель LessonMaterial
- [x] Создать модель Assignment
- [x] Создать модель AssignmentFile
- [x] Создать модель Submission
- [x] Создать модель SubmissionFile
- [x] Создать модель Grade
- [x] Создать модель Comment
- [x] Создать модель Notification
- [x] Создать модель Feedback
- [x] Создать модель ActivityLog
- [x] Выполнить миграции

### 4. Backend - Сериализаторы

- [x] UserRegistrationSerializer
- [x] UserProfileSerializer
- [x] CourseSerializer + CourseDetailSerializer
- [x] LessonSerializer + LessonDetailSerializer
- [x] AssignmentSerializer
- [x] SubmissionSerializer + SubmissionWithFilesSerializer
- [x] GradeSerializer
- [x] CommentSerializer
- [x] FeedbackSerializer
- [x] NotificationSerializer
- [x] Документация сериализаторов (SERIALIZERS_GUIDE.md)

### 5. Backend - Permissions

- [ ] IsTeacher
- [ ] IsStudent
- [ ] IsOwner
- [ ] IsCourseOwner
- [ ] IsTeacherOrReadOnly

### 6. Backend - API Views/ViewSets

- [ ] Authentication endpoints (register, login, refresh, profile)
- [ ] Courses ViewSet (CRUD + enroll)
- [ ] Lessons ViewSet (CRUD)
- [ ] Assignments ViewSet (CRUD)
- [ ] Submissions ViewSet (CRUD)
- [ ] Grades ViewSet (CRUD)
- [ ] Comments ViewSet (CRUD)
- [ ] Notifications ViewSet (list + mark as read)
- [ ] Feedback ViewSet (POST для пользователей, GET для админа)
- [ ] Categories ViewSet (read-only)

### 7. Backend - URLs

- [ ] Настроить роутинг для всех ViewSets
- [ ] Добавить JWT endpoints
- [ ] Документация API (опционально - drf-spectacular)

### 8. Backend - Celery Tasks

- [ ] Task для email-уведомлений о дедлайнах
- [ ] Task для уведомлений о новых оценках
- [ ] Task для уведомлений о новых комментариях
- [ ] Periodic task (beat) для проверки дедлайнов
- [ ] Настроить Celery в settings.py

### 9. Backend - Django Admin

- [x] Зарегистрировать все модели в admin.py
- [x] Настроить list_display, list_filter, search_fields
- [x] Добавить inline редактирование где нужно

### 10. Backend - Тесты

- [ ] Тесты моделей
- [ ] Тесты API endpoints
- [ ] Тесты permissions
- [ ] Тесты сериализаторов

### 11. Frontend - Базовая настройка

- [ ] Настроить `nuxt.config.ts`:
  - [ ] Nuxt UI
  - [ ] Pinia
  - [ ] Runtime config для API URL
  - [ ] Middleware
- [ ] Установить дополнительные пакеги (zod, @vueuse/core)

### 12. Frontend - Composables

- [ ] `useAuth.ts` (авторизация, JWT)
- [ ] `useApi.ts` (базовый API клиент)
- [ ] `useCourses.ts`
- [ ] `useLessons.ts`
- [ ] `useAssignments.ts`
- [ ] `useSubmissions.ts`
- [ ] `useGrades.ts`
- [ ] `useComments.ts`
- [ ] `useFeedback.ts`
- [ ] `useNotifications.ts`
- [ ] `useFileUpload.ts`

### 13. Frontend - Stores (Pinia)

- [ ] `auth.ts` (user, role, token, login/logout)
- [ ] `courses.ts` (courses list, filters, sorting)
- [ ] `lessons.ts`
- [ ] `notifications.ts` (notifications, unreadCount)

### 14. Frontend - Validation Schemas (Zod)

- [ ] `auth.schema.ts`
- [ ] `profile.schema.ts`
- [ ] `course.schema.ts`
- [ ] `lesson.schema.ts`
- [ ] `assignment.schema.ts`
- [ ] `comment.schema.ts`
- [ ] `submission.schema.ts`
- [ ] `feedback.schema.ts`

### 15. Frontend - Middleware

- [ ] `auth.ts` (проверка авторизации)
- [ ] `teacher-only.ts`
- [ ] `student-only.ts`
- [ ] `owner.ts`

### 16. Frontend - UI Components

- [ ] Button, Input, Textarea (базовые)
- [ ] FileUpload (с drag&drop)
- [ ] Modal, Card, Badge
- [ ] Forms:
  - [ ] RegisterForm
  - [ ] LoginForm
  - [ ] ProfileEditForm
  - [ ] CommentForm
  - [ ] SubmissionForm
  - [ ] FeedbackForm
  - [ ] CourseForm
  - [ ] LessonForm
  - [ ] AssignmentForm
- [ ] Course components:
  - [ ] CourseCard
  - [ ] CourseFilter
  - [ ] LessonList
- [ ] Lesson components:
  - [ ] LessonContent
  - [ ] CommentList
  - [ ] AssignmentList
- [ ] Dashboard components:
  - [ ] TeacherStats
  - [ ] StudentProgress
  - [ ] UpcomingDeadlines

### 17. Frontend - Pages

- [ ] `index.vue` (главная)
- [ ] `auth/login.vue`
- [ ] `auth/register.vue`
- [ ] `dashboard/index.vue` (роутинг по ролям)
- [ ] `dashboard/teacher.vue`
- [ ] `dashboard/student.vue`
- [ ] `courses/index.vue` (список курсов)
- [ ] `courses/[id].vue` (детали курса)
- [ ] `courses/create.vue`
- [ ] `lessons/[id].vue`
- [ ] `assignments/[id].vue`
- [ ] `profile/index.vue`
- [ ] `feedback.vue`

### 18. Интеграция и тестирование

- [ ] Проверка работы регистрации/авторизации
- [ ] Проверка CRUD операций для курсов
- [ ] Проверка отправки заданий студентами
- [ ] Проверка выставления оценок преподавателями
- [ ] Проверка системы комментариев
- [ ] Проверка уведомлений (Celery)
- [ ] Проверка загрузки файлов

### 19. Документация

- [ ] API документация (Swagger/ReDoc)
- [ ] Обновить README.md с примерами использования
- [ ] Инструкции по развертыванию

### 20. Production готовность

- [ ] Настроить production settings для Django
- [ ] Настроить SSL для Nginx
- [ ] Настроить логирование
- [ ] Backup стратегия для SQLite
- [ ] Мониторинг и алерты

4. Frontend auth + dashboard
5. Базовые CRUD операции

**Важные:** 6. Permissions и security 7. Файловая загрузка 8. Комментарии и уведомления 9. Celery tasks

**Опциональные:** 10. Тесты 11. API документация 12. Production optimization
