# Промт: Реализация страницы урока и задания урока для преподавателя

## ✅ ЗАВЕРШЕНО

Все задачи из этого промта успешно реализованы.

## Архитектурное решение

- **Frontend**: Nuxt 3 с Composition API, TypeScript Strict, Nuxt UI компоненты
- **Backend**: Django REST Framework с ViewSets, Foreign Key для заданий к урокам
- **State**: Pinia для глобального стейта, локальный стейт в composables
- **Валидация**: Zod для форм, серверная валидация через DRF
- **UI**: Apple-like минимализм, микро-анимации, адаптивность

## Реализованные компоненты

### Схемы (schemas/)

- ✅ `schemas/lessons.schema.ts`: Zod схема для валидации уроков
- ✅ `schemas/assignments.schema.ts`: Zod схема для валидации заданий

### Composables

- ✅ `useLessons.ts`: CRUD операции с optimistic updates для преподавателя
- ✅ `useLessonController.ts`: Управление уроками для студентов
- ✅ `useAssignments.ts`: Управление заданиями для студентов
- ✅ `useTeacher.ts`: Панель управления преподавателя

### Компоненты (components/)

- ✅ `teacher/lessons/Form.vue`: Форма создания/редактирования урока
- ✅ `teacher/lessons/List.vue`: Список уроков курса с действиями
- ✅ `teacher/assignments/Form.vue`: Форма создания/редактирования задания
- ✅ `teacher/assignments/List.vue`: Список заданий с фильтрацией

### Страницы (pages/)

- ✅ `teacher/courses/[slug]/lessons/index.vue`: Список уроков (использует TeacherLessonsList)
- ✅ `teacher/courses/[slug]/lessons/create.vue`: Создание урока (использует TeacherLessonsForm)
- ✅ `teacher/courses/[slug]/lessons/[lesson_slug]/index.vue`: Просмотр урока
- ✅ `teacher/courses/[slug]/lessons/[lesson_slug]/edit.vue`: Редактирование урока (использует TeacherLessonsForm)
- ✅ `teacher/courses/[slug]/assignments/index.vue`: Список заданий (использует TeacherAssignmentsList)
- ✅ `teacher/courses/[slug]/assignments/create.vue`: Создание задания (использует TeacherAssignmentsForm)
- ✅ `teacher/courses/[slug]/assignments/[id]/index.vue`: Просмотр задания
- ✅ `teacher/courses/[slug]/assignments/[id]/edit.vue`: Редактирование задания (использует TeacherAssignmentsForm)

## Критерии приемки

- [x] Преподаватель может просматривать урок
- [x] Преподаватель может редактировать урок
- [x] Преподаватель может создавать задания к уроку
- [x] Преподаватель может редактировать задания
- [x] Преподаватель может удалять задания
- [x] Интеграция с комментариями работает
- [x] Созданы недостающие компоненты форм
- [x] Реализован useLessons composable
- [x] Создана схема валидации уроков
- [x] UI соответствует дизайну системы
- [x] Все формы валидируются корректно
- [x] Ролевая защита работает

## Файлы созданные в этой сессии

1. `/client/app/schemas/lessons.schema.ts`
2. `/client/app/composables/useLessons.ts`
3. `/client/app/components/teacher/lessons/Form.vue`
4. `/client/app/components/teacher/lessons/List.vue`
5. `/client/app/components/teacher/assignments/Form.vue`
6. `/client/app/components/teacher/assignments/List.vue`
7. `/client/app/pages/teacher/courses/[slug]/lessons/[lesson_slug]/index.vue`
8. `/client/app/pages/teacher/courses/[slug]/assignments/[id]/index.vue`
9. Обновлены все страницы в `pages/teacher/courses/[slug]/lessons/` и `pages/teacher/courses/[slug]/assignments/`
