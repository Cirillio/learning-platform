# Задачи по рефакторингу Learning Platform

## Phase 1: Routing Refactor (The "Learning Mode")

- [x] 1.1 Создать структуру маршрутов `/learning/`
- [x] 1.2 Рефакторинг `/courses/[slug]/index.vue` — Marketing Page
- [x] 1.3 Создать `/learning/[course_slug]/index.vue` — Course Dashboard
- [x] 1.4 Создать `/learning/[course_slug]/lessons/[lesson_slug].vue` — Lesson Player
- [x] 1.5 Создать `/learning/[course_slug]/assignments/index.vue` — List of assignments
- [x] 1.6 Создать `/learning/[course_slug]/assignments/[assignment_id].vue` — Assignment details
- [x] 1.7 Создать Learning Layout (минимальный header, collapsible sidebar)

## Phase 2: Assignments Implementation (Student Side)

- [x] 2.1 Обновить `types/index.ts` — Assignment, Submission, AssignmentFile
- [x] 2.2 Создать `services/assignments.ts` — fetchAssignments, submitAssignment
- [x] 2.3 Создать `services/submissions.ts` — uploadSubmissionFile
- [x] 2.4 Создать Zod-схемы для Assignment и Submission
- [x] 2.5 Реализовать UI Assignment Details Component
- [x] 2.6 Реализовать Submission Form с логикой состояний (graded/pending/none)
- [x] 2.7 Реализовать File Upload компонент с drag & drop

## Phase 3: Teacher Dashboard & Functionality

- [x] 3.1 Создать middleware для проверки роли teacher
- [x] 3.2 Создать Teacher Layout
- [x] 3.3 Создать `/teacher/index.vue` — Dashboard Home
- [x] 3.4 Создать `/teacher/courses/index.vue` — List of courses
- [x] 3.5 Создать `/teacher/courses/create.vue` — Create Course Form
- [x] 3.6 Создать `/teacher/courses/[slug]/edit.vue` — Edit Course Form
- [x] 3.7 Создать `/teacher/courses/[slug]/lessons/index.vue` — Lesson Management
- [x] 3.8 Создать `/teacher/courses/[slug]/assignments/index.vue` — Assignment Management
- [x] 3.9 Создать `/teacher/grading/index.vue` — Gradebook
- [x] 3.10 Реализовать Grading Interface (modal/detailed view)

## Дополнительно реализовано:

- [x] `/teacher/courses/[slug]/lessons/create.vue` — Создание урока
- [x] `/teacher/courses/[slug]/lessons/[lesson_slug]/edit.vue` — Редактирование урока
- [x] `/teacher/courses/[slug]/assignments/create.vue` — Создание задания
- [x] `/teacher/courses/[slug]/assignments/[id]/edit.vue` — Редактирование задания

## Composables & Services

- [x] 4.1 Создать `composables/useAssignments.ts`
- [x] 4.2 Создать `services/useSubmissionsService.ts`
- [x] 4.3 Создать `composables/useTeacher.ts`
- [x] 4.4 Создать `services/useTeacherService.ts`

## Components

- [x] 5.1 Создать `components/learning/sidebar.vue`
- [x] 5.2 Создать `components/learning/header.vue`
- [x] 5.3 Создать `components/assignments/assignment-card.vue`
- [x] 5.5 Создать `components/assignments/file-upload.vue`
- [x] 5.8 Создать `components/teacher/grade-form.vue`
- [x] 5.9 Создать `components/teacher/submission-viewer.vue`

---

**Статус:** ✅ ЗАВЕРШЕНО  
**Последнее обновление:** 2025-01-XX

---

# Phase 4: Design System Refactoring & Component Atomicity

## Анализ и план рефакторинга страниц

### Категория: Auth (✅ ЗАВЕРШЕНО)

- [x] `pages/auth/login.vue` — Заменены text-gray-\* на text-default/text-muted
- [x] `pages/auth/register.vue` — Заменены text-gray-\* на text-default/text-muted
- [x] `pages/auth/logout.vue` — Заменены gray-\* на семантические цвета

### Категория: Settings (✅ ЗАВЕРШЕНО)

- [x] `pages/settings/index.vue` — Создана полноценная страница (тема, язык, аккаунт)
- [x] `pages/settings/notifications.vue` — Реализован UI (email/push/marketing toggles)
- [x] `pages/settings/privacy.vue` — Реализован UI (visibility, 2FA, danger zone)
- [x] `pages/settings/billing.vue` — Реализован UI (планы, методы оплаты, история)
- [x] `pages/settings/account.vue` — Хороший код, без изменений

### Категория: Components Color Fix (✅ ЗАВЕРШЕНО)

- [x] `components/profile/header.vue` — Заменены text-gray-900/400 на text-default/text-muted
- [x] `components/profile/courses-list.vue` — Заменены text-gray-900 на text-default
- [x] `components/courses/catalog/category-grid.vue` — Заменены bg-gray-_, text-gray-_ на bg-elevated, text-muted

### Категория: Learning (✅ ЗАВЕРШЕНО)

- [x] `pages/learning/[course_slug]/index.vue` — Декомпозиция: LearningCourseHero, LearningStatsGrid, LearningLessonsList
- [x] `pages/learning/[course_slug]/lessons/[lesson_slug].vue` — Хороший код, без изменений
- [x] `pages/learning/[course_slug]/assignments/index.vue` — Хороший код, без изменений
- [x] `pages/learning/[course_slug]/assignments/[assignment_id].vue` — Декомпозиция на 5 компонентов:
  - `components/assignments/header.vue`
  - `components/assignments/instructions-card.vue`
  - `components/assignments/files-list.vue`
  - `components/assignments/grade-result.vue`
  - `components/assignments/submission-form.vue`

### Категория: Teacher (✅ ЗАВЕРШЕНО)

- [x] `pages/teacher/index.vue` — Декомпозиция: TeacherWelcomeHero, TeacherStatsGrid, TeacherSubmissionsList, TeacherCoursesSidebar
- [x] `pages/teacher/courses/index.vue` — Хороший код, без изменений
- [x] `pages/teacher/courses/create.vue` — Хороший код, без изменений
- [x] `pages/teacher/courses/[slug]/index.vue` — Декомпозиция на 5 компонентов:
  - `components/teacher/course-header.vue`
  - `components/teacher/course-stats.vue`
  - `components/teacher/lessons-tab.vue`
  - `components/teacher/assignments-tab.vue`
  - `components/teacher/add-lesson-modal.vue`
- [x] `pages/teacher/courses/[slug]/edit.vue` — Хороший код, без изменений
- [x] `pages/teacher/grading/index.vue` — Хороший код, без изменений
- [x] `pages/teacher/grading/[id].vue` — Хороший код, без изменений

---

## Итоги рефакторинга Phase 4

### Созданные компоненты (14 файлов):

**Learning domain:**

- `components/learning/course-hero.vue`
- `components/learning/stats-card.vue`
- `components/learning/stats-grid.vue`
- `components/learning/lessons-list.vue`

**Assignments domain:**

- `components/assignments/header.vue`
- `components/assignments/instructions-card.vue`
- `components/assignments/files-list.vue`
- `components/assignments/grade-result.vue`
- `components/assignments/submission-form.vue`

**Teacher domain:**

- `components/teacher/welcome-hero.vue`
- `components/teacher/stats-grid.vue`
- `components/teacher/submissions-list.vue`
- `components/teacher/courses-sidebar.vue`
- `components/teacher/course-header.vue`
- `components/teacher/course-stats.vue`
- `components/teacher/lessons-tab.vue`
- `components/teacher/assignments-tab.vue`
- `components/teacher/add-lesson-modal.vue`

### Страницы сокращены:

| Файл                               | До         | После      | Сокращение |
| ---------------------------------- | ---------- | ---------- | ---------- |
| `learning/[course_slug]/index.vue` | ~230 строк | ~100 строк | -57%       |
| `learning/.../[assignment_id].vue` | 586 строк  | ~190 строк | -68%       |
| `teacher/index.vue`                | ~321 строк | ~120 строк | -63%       |
| `teacher/courses/[slug]/index.vue` | 550 строк  | ~180 строк | -67%       |

### Исправления Design System:

- ✅ Все `text-gray-*` заменены на `text-default` / `text-muted`
- ✅ Все `bg-gray-*` заменены на `bg-elevated` / `bg-muted/10`
- ✅ Все `border-gray-*` заменены на `border-default`
- ✅ Grep-поиск по `pages/**` и `components/**` возвращает 0 совпадений

**Статус:** ✅ PHASE 4 ЗАВЕРШЕНА  
**Последнее обновление:** 2025-01-XX

### Категория: Courses (Низкий приоритет - уже отрефакторены)

- [x] `pages/courses/index.vue` — Эталон, Gold Standard
- [x] `pages/courses/[slug]/index.vue` — Эталон, Gold Standard
- [x] `pages/courses/categories.vue` — Хороший код

### Глобальные задачи

- [ ] Создать компоненты `components/learning/course-hero.vue`
- [ ] Создать компоненты `components/learning/stats-card.vue`
- [ ] Создать компоненты `components/learning/lessons-list.vue`
- [ ] Создать компоненты `components/teacher/stats-grid.vue`
- [ ] Создать компоненты `components/teacher/course-card.vue`
- [ ] Заменить все `text-gray-*`, `bg-gray-*`, `border-gray-*` на семантические цвета

---

**Статус:** 🚧 В ПРОЦЕССЕ  
**Текущая фаза:** Phase 4 - Design System Refactoring
**Последнее обновление:** 2025-12-12
