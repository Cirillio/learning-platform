# Архитектура фронтенда

Nuxt 4 · Vue 3.5 · TypeScript strict · Pinia · Nuxt UI 4 · Tailwind CSS 4 · Zod.
Рендеринг — SSR. API — Django по адресу `runtimeConfig.public.apiBase`
(`NUXT_PUBLIC_API_BASE`, по умолчанию `http://localhost:8000/api`).

## Слои

```
pages ──► components ──► composables ──► services ──► useApi ($fetch)
                │              │
                └── schemas (Zod), types, utils, constants
stores (Pinia) — только глобальное состояние (сессия пользователя)
```

| Слой | Папка | Правило |
| :--- | :--- | :--- |
| Pages | `app/pages/` | Маршрут, `definePageMeta` (layout, middleware), сборка компонентов. Без бизнес-логики. |
| Components | `app/components/<feature>/` | UI, сгруппирован по фичам. «Глупые» компоненты получают данные через props. |
| Composables | `app/composables/` | Загрузка данных и логика фичи: `useAuth`, `useLessons`, `useTeacher`, `use-comments`… |
| Services | `app/services/*-service.ts` | Типизированные вызовы API, по одному на домен. Автоимпорт (`imports.dirs: ["services"]`), экспорт через `services/index.ts`. |
| API-клиент | `composables/useApi.ts` | `$fetch` с `credentials: "include"`, проброс cookies на SSR, refresh при 401. |
| Schemas | `app/schemas/*.schema.ts` | Zod-схемы форм и ответов API. |
| Types | `app/types/` | Доменные типы, единая точка экспорта `types/index.ts`. |
| Stores | `app/stores/auth.ts` | Pinia: только пользователь и статус загрузки. Токенов нет. |
| Utils / constants | `app/utils/`, `app/constants/` | Чистые функции (форматирование, дерево комментариев) и константы (фильтры каталога, меню). |

## Правила кода

- Только `<script setup lang="ts">`, без Options API. Без `any`.
- Props типизируются через `defineProps<{ … }>()`.
- Размер файла: больше 200 строк — повод декомпозировать, больше 300 — обязательно.
  Порядок: загрузку данных — в `composables/use-<feature>.ts`, вычисления — в `utils/`,
  части шаблона — в `components/<feature>/<part>.vue`.
- Состояние: Pinia — глобальное (сессия); `useState` в composable — состояние фичи;
  `ref` — локальный UI (модалки, дропдауны).
- Имена файлов — `kebab-case`: `assignment-card.vue`, `use-teacher-lesson.ts`,
  `courses-service.ts`, `auth.schema.ts`, `formatters.util.ts`. Nuxt сам превращает
  `assignment-card.vue` в `<AssignmentCard />`. Часть старых composables ещё в camelCase
  (см. `context/roadmap.md`).

## UI

- Компоненты — Nuxt UI 4, стили — утилиты Tailwind; кастомный CSS только если без него не обойтись.
- Цвета темы задаются в `app.config.ts` (`primary`, `secondary`, `accent`, `neutral`, статусные).
  Шрифт — Mulish (`@nuxtjs/google-fonts`).
- Светлая и тёмная темы. Скелетоны при загрузке (`components/skeletons/`), пустые
  состояния и ошибки обрабатываются явно.
- Эталон вёрстки — страницы преподавателя (`pages/teacher/`, `components/teacher/`).

## Маршруты и доступ

| Маршрут | Layout | Middleware | Назначение |
| :--- | :--- | :--- | :--- |
| `/` | default | — | Лендинг |
| `/auth/login`, `/auth/register` | auth | `guest` | Вход, регистрация |
| `/auth/logout` | — | — | Выход |
| `/courses`, `/courses/categories`, `/courses/[slug]` | default | — | Каталог, категории, страница курса |
| `/dashboard` | — | редирект | 301 на `/learning` |
| `/learning`, `/learning/grades` | default | `auth`, `student-only` | Кабинет студента, журнал оценок |
| `/learning/[course_slug]/…` | default | `auth`, `enrolled-course` | Курс, уроки, задания (только записанным) |
| `/profile` | default | `auth`, `profile-redirect` | Профиль студента; преподаватель уходит на `/teacher` |
| `/settings/*` | settings | — | Настройки аккаунта |
| `/teacher/**` | teacher | `teacher-only` | Панель преподавателя: курсы, уроки, задания, проверка работ |

Middleware (`app/middleware/`):

- `auth` — нет пользователя → `/auth/login?redirectTo=…`.
- `guest` — авторизованного уводит с `/auth/*` на `/profile`.
- `student-only`, `teacher-only` — проверка роли, иначе редирект.
- `enrolled-course` — запрашивает курс и пускает только при `is_enrolled`, иначе на страницу курса.
- `profile-redirect` — разводит профиль по ролям.

## Каталог курсов

Фильтры синхронизируются с query-параметрами URL через `useCourseFilters`; URL — источник
истины. Компонент фильтров держит черновик локально и применяет изменения по кнопке
(или Enter в поиске). Смена любого фильтра, кроме страницы, сбрасывает пагинацию на 1.
Значения по умолчанию — в `constants/courseFilters.ts` (6 курсов на страницу,
сортировка `-created_at`).
