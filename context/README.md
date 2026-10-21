# Контекст проекта

Точка входа для разработчика и AI-агента. Здесь собрано то, что нельзя быстро понять
из кода: устройство системы, договорённости и открытые задачи.

## Карта документов

| Документ | О чём |
| :--- | :--- |
| [context/README.md](README.md) | Этот файл: обзор, домен, общие правила. |
| [context/api.md](api.md) | Справочник REST API: эндпоинты, тела запросов, ответы. |
| [context/roadmap.md](roadmap.md) | Открытые задачи и известные проблемы. |
| [client/context/architecture.md](../client/context/architecture.md) | Фронтенд: слои, именование, маршруты, состояние, UI. |
| [client/context/auth.md](../client/context/auth.md) | Авторизация: cookies, SSR, refresh, middleware. |
| [client/context/testing.md](../client/context/testing.md) | Ручной чек-лист проверки сценариев. |
| [server/context/architecture.md](../server/context/architecture.md) | Бэкенд: приложения, модели, права, Celery. |
| [server/context/dev-guide.md](../server/context/dev-guide.md) | Запуск, демо-данные, тесты, полезные команды. |

## Что это

LMS (учебный портал) с двумя ролями:

- **Студент**: каталог → запись на курс → уроки → сдача заданий → оценки.
- **Преподаватель**: создаёт курсы, уроки и задания, проверяет работы, ставит баллы.

Стек: Nuxt 4 (SSR) + Django REST Framework, SQLite, Celery + Redis, Docker + Nginx.

```
Browser ──► Nuxt 4 (SSR, :3000) ──► Django REST API (:8000/api) ──► SQLite
                                         └──► Celery worker / beat ──► Redis
```

## Домен

```
Category ─┐
          Course ──< Lesson ──< Assignment ──< Submission ── Grade
            │          └──< LessonMaterial      └──< SubmissionFile
            └──< CourseEnrollment >── User (student)
User (teacher) ──< Course
Comment ── GenericFK → Lesson (и любые другие модели), дерево через parent
Notification, Feedback, ActivityLog — служебные
```

- Курс: статусы `draft / published / archived`, сложность `beginner / intermediate / …`.
- Ответ на задание: статусы `pending / graded / returned`.
- Задание принадлежит уроку, урок — курсу. Фильтрация заданий идёт по уроку.

## Общие правила

- **Типобезопасность.** TypeScript strict, без `any`. Ответы API и формы валидируются через Zod.
- **Тонкие страницы.** Логика живёт в composables/services (фронт) и services/models (бэк).
- **Лимит размера файла.** Больше 200 строк — повод декомпозировать; больше 300 — обязательно.
- **Именование.** Фронт — `kebab-case` для файлов, бэк — стандарт Python.
- **Коммиты.** Conventional Commits: `feat: …`, `fix: …`, `refactor: …`, `docs: …`.
- **Секреты.** Только в `.env` (в git не попадает). Примеры — в `*.env.example`.
