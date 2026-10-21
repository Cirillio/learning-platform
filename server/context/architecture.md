# Архитектура бэкенда

Django 5.2 · Django REST Framework · SimpleJWT · Celery + Redis · SQLite.
Справочник эндпоинтов — [context/api.md](../../context/api.md).

## Приложения

| Приложение | Модели | URL-префикс |
| :--- | :--- | :--- |
| `users` | `User` (наследник `AbstractUser`, поле `role`: `student` / `teacher`), `UserProfile` (аватар, био, телефон, дата рождения, адрес) | `/api/auth/…`, `/api/users/` |
| `courses` | `Category`, `Course`, `CourseEnrollment`, `Lesson`, `LessonMaterial`, `Assignment`, `AssignmentFile`, `Submission`, `SubmissionFile`, `Grade` | `/api/courses/`, `/lessons/`, `/assignments/`, `/submissions/`, `/grades/`, `/categories/` |
| `core` | `Comment` (Generic FK + `parent` для дерева ответов), `Feedback`, `ActivityLog` | `/api/core/…` |
| `notifications` | `Notification` | `/api/notifications/` |
| `config` | settings, корневые urls, Celery | — |

`UserProfile` создаётся сигналом `users/signals.py` при создании пользователя.

## Модели: ключевые связи

- `Course.teacher → User`; статусы `draft / published / archived`, поиск по `slug`.
- `CourseEnrollment` — запись студента на курс, хранит прогресс и активность.
- `Lesson → Course` (сортировка по `order`), `LessonMaterial → Lesson`.
- `Assignment → Lesson`; `max_score`, `due_date`, `allow_late_submission`, `is_required`.
- `Submission → Assignment + student`; статусы `pending / graded / returned`, файлы — `SubmissionFile`.
- `Grade → Submission`; балл, комментарий, кто проверил.
- `Comment` привязывается к любой модели через `content_type + object_id`
  (ID берётся из `/api/core/content-types/`).

## Слои

- **Views** — тонкие: парсинг запроса, права, формирование ответа. В основном `ModelViewSet`
  с дополнительными `@action`: `enroll`, `unenroll`, `my_courses`, `students` у курсов;
  `mark_as_read`, `mark_all_as_read`, `unread_count` у уведомлений; `resolve` у обратной связи.
- **Serializers** — валидация входа и формирование JSON, отдельные сериализаторы для списка и деталей.
- **Models** — инварианты данных.
- **Tasks** — побочные эффекты (письма, уведомления) уходят в Celery.

## Права

Глобально — `IsAuthenticated`; публичные эндпоинты явно открывают доступ.

| Класс | Где | Смысл |
| :--- | :--- | :--- |
| `IsTeacher`, `IsStudent` | `users/permissions.py`, `courses/permissions.py` | Проверка роли. |
| `IsOwner` | `courses/permissions.py` | Владелец объекта. |
| `IsCourseOwner` | `courses/permissions.py` | Преподаватель — автор курса (для уроков, заданий и проверки). |
| `IsTeacherOrReadOnly` | `courses/permissions.py` | Чтение всем, запись преподавателю. |
| `IsAdminUser` | DRF | Модерация обратной связи. |

Комментарии может менять и удалять только автор; обращения в обратную связь пользователь
видит только свои, администратор — все.

## Аутентификация

- `LoginView` / `RefreshTokenView` / `LogoutView` ставят и удаляют HttpOnly-cookies
  `access_token`, `refresh_token`, `auth_remember_me` (`Secure`, `SameSite=Lax`).
- `users.middleware.JWTAuthFromCookieMiddleware` копирует access-токен из cookie в
  `Authorization: Bearer …` — дальше работает стандартный `JWTAuthentication`.
- Access — 15 минут, refresh — 7 дней (30 при `remember_me`), ротация с blacklist.

Клиентская сторона — [client/context/auth.md](../../client/context/auth.md).

## Настройки API

- Пагинация `PageNumberPagination`, 20 элементов, `?page=` / `?page_size=`.
- Фильтры `SearchFilter` (`?search=`) и `OrderingFilter` (`?ordering=`).
- Опции фильтров каталога отдаёт `GET /api/courses/filters/`.
- CORS: `CORS_ALLOWED_ORIGINS` (`localhost:3000`, `localhost:3001`), `CORS_ALLOW_CREDENTIALS = True`.

## Celery

Брокер и backend результатов — `REDIS_URL`.

| Задача | Когда |
| :--- | :--- |
| `users.tasks.send_login_notification_email` | При каждом входе. |
| `courses.tasks.send_new_assignment_notification` | Новое задание. |
| `courses.tasks.send_grade_notification` | Выставлена оценка. |
| `core.tasks.send_comment_notification` | Новый комментарий. |
| `notifications.tasks.send_notification_email` | Письмо по уведомлению. |
| `courses.tasks.check_assignment_deadlines` | Beat: каждый час. |
| `notifications.tasks.send_pending_email_notifications` | Beat: каждые 15 минут. |
| `users.tasks.clear_blacklisted_tokens` | Beat: ежедневно в полночь. |
| `notifications.tasks.cleanup_old_notifications` | Вручную / по расписанию в админке (`django_celery_beat`). |

## Обратная связь

`core.Feedback`: типы `bug / feature / improvement / question / other`, статусы
`new / in_progress / resolved / closed`, приоритет, скриншот, ответ администратора.
На фронте — `components/feedback/feedback-dialog.vue`, `useFeedback`, `feedback-service`.
