# University LMS Architecture & Guidelines

Этот документ описывает архитектурные стандарты, соглашения об именовании и правила разработки для проекта University LMS.
Все участники проекта обязаны следовать этим правилам для поддержания качества и масштабируемости кода.

## 1. Core Principles (Основные принципы)
*   **Role:** Senior Enterprise LMS.
*   **Stack:** Nuxt 4 (Vue 3, TypeScript), Django REST Framework, Docker.
*   **Philosophy:** "Fat Models/Services, Thin Views". UI должен быть максимально "глупым"; вся бизнес-логика инкапсулируется в Services или Composables.

## 2. Naming Conventions (Соглашения об именовании)

### Frontend (Client)
Все файлы на фронтенде используют **kebab-case**.

*   **Vue Components:** `kebab-case.vue` (например, `assignment-card.vue`, `user-profile.vue`).
    *   *Nuxt Auto-import:* Nuxt автоматически маппит `assignment-card.vue` в `<AssignmentCard />`.
*   **Composables:** `use-kebab-case.ts` (например, `use-auth.ts`, `use-teacher-actions.ts`).
    *   *Usage:* В коде используется camelCase: `const { login } = useAuth()`.
*   **Services (API/Logic):** `kebab-case.service.ts` (например, `auth.service.ts`, `payment-gateway.service.ts`).
*   **Types/Schemas:** `kebab-case.types.ts` или `kebab-case.schema.ts`.
*   **Utils:** `kebab-case.util.ts`.

### Backend (Server)
*   **Python Modules:** `snake_case.py` (Стандарт Python).
*   **Classes:** `PascalCase` (например, `AssignmentSerializer`).
*   **Variables/Functions:** `snake_case`.

## 3. Frontend Architecture (Nuxt)

### A. Component Structure
*   **Script:** Только `<script setup lang="ts">`. Options API запрещен.
*   **Style:** Избегать кастомного CSS. Использовать Tailwind CSS утилиты.
*   **Size Limit (Лимиты размера файла):**
    *   **Warning:** > 200 строк.
    *   **Refactor Required:** > 300 строк.
*   **Props:** Всегда типизированы через `defineProps<{ ... }>()` или импортированный интерфейс.

### B. Logic Separation (Правила рефакторинга)
Если компонент превышает лимит строк:
1.  **Data Fetching** -> Выносим в `composables/use-feature-data.ts`.
2.  **Complex Computation** -> Выносим в `utils/` или `composables/`.
3.  **UI Parts** -> Декомпозируем в `components/feature/part-name.vue`.

### C. State Management
*   **Pinia:** Только для глобального стейта (Сессия пользователя, Тема, Уведомления).
*   **Composables (useState):** Для шаринга состояния внутри конкретной фичи/страницы.
*   **Local Ref:** Для локального UI состояния (открытие модалок, дропдаунов).

## 4. Backend Architecture (Django)

### A. Layers (Слои)
1.  **Views (API):** Экстремально тонкие. Только парсинг запроса и форматирование ответа.
2.  **Services/Selectors:** Бизнес-логика живет здесь (e.g., `services.py`, `selectors.py` в приложениях).
3.  **Models:** "Богатые" модели. Инкапсулируют правила целостности данных.
4.  **Serializers:** Валидация входных данных и формирование JSON.

## 5. Development Workflow
1.  **Type Safety:** `any` запрещен. Использовать Zod для валидации API ответов.
2.  **Commits:** Conventional Commits (например, `feat: add lesson editor`, `fix: assignment submission error`).
