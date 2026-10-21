# Открытые задачи

Собрано из старых планов (`NEXT_STEPS.md`, `REFACTOR_PLAN.md`, `todo-s/`) и сверено с кодом.
Выполненное удалено.

## Рефакторинг фронтенда

Файлы, которые превышают лимит в 300 строк:

| Файл | Строк | Что сделать |
| :--- | ---: | :--- |
| `pages/teacher/courses/[slug]/edit.vue` | 443 | Вместе с `create.vue` вынести общую форму в `components/teacher/courses/course-form.vue`, логику — в `composables/use-course-form.ts`. На страницах оставить только вызов формы. |
| `pages/teacher/courses/create.vue` | 372 | См. выше. |
| `pages/learning/[course_slug]/lessons/[lesson_slug].vue` | 399 | Разбить на плеер, навигацию «назад/вперёд/завершить» и сайдбар со списком уроков (`components/learning/lesson/`). |
| `composables/useLessons.ts` | 386 | Разделить сценарии студента и преподавателя. |
| `composables/use-comments.ts` | 378 | Разделить загрузку, локальное состояние и мутации. |
| `pages/settings/billing.vue` | 314 | Вынести историю платежей и способы оплаты в `components/settings/billing/`. |

Сквозные задачи:

- Общий тип `PaginatedResponse<T>` вместо отдельных `CoursesResponse`, `SubmissionsResponse` и т. п.
- Заменить инлайновые `toLocaleDateString` и расчёты размера файлов на `utils/formatters.util.ts`.
- Привести имена composables к `kebab-case` (`useLessons.ts` → `use-lessons.ts` и т. д.).
- Убрать отладочные `console.log` из `plugins/auth.ts` и `server/middleware/auth.ts`.

## Известные проблемы

- **Контент урока не рендерится как Markdown.** Материал урока выводится сырым текстом
  (`# Урок 1 ## …`). Нужен рендер Markdown с санитизацией.
- **Страницы `/settings/*` без middleware `auth`.** Гость может открыть их напрямую;
  нужно добавить `middleware: ["auth"]` в `definePageMeta` или в layout `settings`.
- **Вход зависает без Redis.** Логин ставит Celery-задачу (письмо о входе), и без брокера
  запрос висит. Варианты: `CELERY_TASK_ALWAYS_EAGER` в dev или таймаут подключения к брокеру.
- **Профиль преподавателя.** `profile-redirect` отправляет преподавателя на `/teacher`;
  отдельной страницы `/teacher/profile` нет.

## Возможные улучшения

- Ответы на комментарии: ограничить вложенность тремя уровнями, добавить пагинацию.
- Обратная связь: уведомление администратору о новом обращении, история статусов.
- Автотесты фронтенда (сейчас проверка только ручная — см. `client/context/testing.md`).
