# Компоненты курсов

## Константы

Все константы для фильтров и пагинации курсов централизованы в `~/constants/courseFilters.ts`:

- `COURSE_PAGE_SIZE_DEFAULT = 6` - размер страницы по умолчанию
- `COURSE_ORDERING_DEFAULT = "-created_at"` - сортировка по умолчанию
- `COURSE_PAGE_SIZE_MIN = 6` - минимальный размер страницы
- `COURSE_PAGE_SIZE_MAX = 50` - максимальный размер страницы
- `COURSE_SEARCH_PLACEHOLDER = "Поиск курсов..."` - плейсхолдер для поиска
- `COURSE_CACHE_KEY_PREFIX = "courses"` - префикс для ключей кэша
- `COURSE_FILTER_DEFAULTS` - объект со всеми значениями по умолчанию

Используйте эти константы вместо жестко закодированных значений для обеспечения 一致 ности.

Этот каталог содержит компоненты, связанные с отображением и управлением курсами.

## Структура компонентов

### CoursesFilters.vue

**Назначение**: Панель фильтров для каталога курсов с локальным состоянием и явным применением изменений.

**Props**:

- `search` (string) - текущее значение поиска из URL
- `category` (string, optional) - текущая выбранная категория из URL
- `difficulty` (string, optional) - текущая выбранная сложность из URL
- `ordering` (string, optional) - текущая выбранная сортировка из URL
- `categoryOptions` (FilterOption[]) - опции категорий для выбора
- `difficultyOptions` (FilterOption[]) - опции сложности для выбора
- `orderingOptions` (FilterOption[]) - опции сортировки для выбора
- `isLoading` (boolean, optional) - состояние загрузки данных

**Events**:

- `apply` - событие применения фильтров, передает объект с текущими значениями:
  ```typescript
  {
    search: string;
    category?: string;
    difficulty?: string;
    ordering?: string;
  }
  ```
- `reset` - событие сброса всех фильтров

**Функционал**:

- **Локальное состояние**: управляет своим внутренним состоянием (черновиками фильтров)
- **Синхронизация**: автоматически синхронизируется с входящими props через watchers
- **Определение изменений**: computed `hasChanges` проверяет, отличаются ли локальные значения от props
- **Кнопка "Применить"**:
  - Активна только если есть изменения (`hasChanges`)
  - Отключается во время загрузки
  - Эмитит событие `apply` с текущими значениями фильтров
  - Поддерживает Enter в поле поиска
- **Кнопка "Очистить"**:
  - Эмитит событие `reset`
  - Отключается во время загрузки
- **UX улучшения**:
  - Все контролы отключаются при `isLoading`
  - Enter в поле поиска применяет фильтры
  - Визуальная индикация возможности применить изменения

**Архитектура**:

Компонент следует паттерну "управляемого компонента" (controlled component):

1. Принимает текущие значения через props (источник истины - URL)
2. Управляет локальным состоянием для редактирования
3. Эмитит события для применения изменений
4. Родительский компонент решает, когда обновлять URL и делать запрос

**Пример использования**:

```vue
<CoursesItemFilters
  :search="searchValue"
  :category="selectedCategory?.value"
  :difficulty="selectedDifficulty?.value"
  :ordering="selectedOrdering?.value"
  :category-options="categoryOptions"
  :difficulty-options="difficultyOptions"
  :ordering-options="orderingOptions"
  :is-loading="pending"
  @apply="handleApplyFilters"
  @reset="handleResetFilters"
/>
```

/>

````

### `item-card.vue`

Карточка отдельного курса для отображения в списке.

**Props**:

- `course` (Course) - объект курса
- `canEnroll` (boolean, optional) - может ли пользователь записаться на курс
- `enrolled` (boolean, optional) - записан ли пользователь на курс

**Функционал**:

- Отображение обложки курса с fallback изображением
- Показ названия, описания и категории курса
- Badges для статуса и сложности с цветовой индикацией
- Информация о преподавателе, количестве студентов, длительности
- Кнопки действий в зависимости от статуса записи:
  - "Записаться" - если пользователь не записан и может записаться
  - "Перейти к курсу" - если пользователь уже записан
  - "Подробнее" - открывает модальное окно с детальной информацией о курсе
- Модальное окно `CoursesItemDetailsModal` с полной информацией о курсе

### `item-details-modal.vue`

Модальное окно с детальной информацией о курсе.

**Props**:

- `course` (Course) - объект курса

**Model**:

- `open` (boolean) - v-model для управления видимостью модального окна

**Функционал**:

- Отображение обложки курса с badges статуса и сложности
- Детальное описание курса
- Информационные карточки с иконками:
  - Преподаватель
  - Категория
  - Длительность (если указана)
  - Количество записанных студентов и лимит (если установлен)
  - Дата создания курса
  - Дата последнего обновления
- Индикатор рекомендуемого курса (если `is_featured = true`)
- Кнопки в футере:
  - "Закрыть" - закрывает модальное окно
  - "Перейти к курсу" - навигация на страницу курса

**Используемые NuxtUI компоненты**:

- `UModal` - основной компонент модального окна
- `UBadge` - для отображения статуса и сложности
- `UIcon` - иконки для информационных блоков
- `UButton` - кнопки действий

### CoursesGrid.vue

**Назначение**: Сетка курсов с обработкой пустого состояния.

**Props**:

- `courses`: Course[] - массив курсов

**Особенности**:

- Отображает сетку курсов (2 колонки)
- Показывает пустое состояние с иконкой, если курсов нет
- Состояние загрузки управляется на уровне страницы

**Пример использования**:

```vue
<script setup lang="ts">
import { COURSE_PAGE_SIZE_DEFAULT } from "~/constants/courseFilters";

const PAGE_SIZE = COURSE_PAGE_SIZE_DEFAULT;
</script>

<template>
  <!-- Скелетоны при загрузке -->
  <div v-if="pending" class="grid grid-cols-2 gap-4">
    <SkeletonsCourseCard v-for="i in PAGE_SIZE" :key="i" />
  </div>

  <!-- Сетка курсов -->
  <CoursesItemGrid v-else :courses="courses" />
</template>
````

## Связанные компоненты

### SkeletonsCourseCardSkeleton.vue

Скелетон для карточки курса, используется во время загрузки данных.

## Архитектура страницы `/courses/all`

Страница использует следующую архитектуру:

1. **Управление состоянием**: Фильтры синхронизируются с URL через query параметры
2. **SSR**: Все данные загружаются на сервере для оптимальной производительности
3. **Реактивность**: Изменение фильтров автоматически обновляет результаты
4. **Пагинация**: Поддержка пагинации через компонент UPagination
5. **Модульность**: Логика разделена на переиспользуемые компоненты

## Типы

Все используемые TypeScript типы определены в `~/types/index.ts`:

### Основные типы курсов:

- `Course` - базовый тип курса для списков
- `CourseDetail` - расширенный тип для детальной страницы

### Типы фильтров:

- `FilterOption` - опция фильтра (value + label)
- `CourseFilterGroup` - группа фильтров с метаданными
- `CourseFiltersResponse` - ответ API с опциями фильтров

### Типы запросов/ответов:

- `CourseFilters` - параметры для фильтрации курсов
- `CoursesResponse` - ответ API со списком курсов + пагинация
- `CategoriesResponse` - ответ API со списком категорий + пагинация

Все типы экспортируются из центрального файла типов и используются во всех компонентах для обеспечения типобезопасности.

## Composables

### useCourses

Основной composable для работы с курсами:

- `getCourses(params)` - получение списка курсов с фильтрами
- `getCourseFilterOptions()` - получение опций для фильтров
- `getCourse(slug)` - получение детальной информации о курсе
- `getMyCourses()` - получение курсов текущего пользователя
- `getCategories()` - получение категорий
- `enrollToCourse(slug)` - запись на курс
- `unenrollFromCourse(slug)` - отмена записи на курс
- Поддержка пагинации через параметры `page` и `page_size`

### useCourseFilters

Composable для управления фильтрами курсов с синхронизацией URL:

**Параметры**:

- `categoryOptions` - ComputedRef с опциями категорий
- `difficultyOptions` - ComputedRef с опциями сложности
- `orderingOptions` - ComputedRef с опциями сортировки
- `options` - объект с настройками:
  - `pageSize` - размер страницы (по умолчанию `COURSE_PAGE_SIZE_DEFAULT = 6`)
  - `defaultOrdering` - сортировка по умолчанию (по умолчанию `COURSE_ORDERING_DEFAULT = "-created_at"`)

**Возвращаемые значения**:

- `searchValue` - текущее значение поиска
- `selectedCategory` - выбранная категория (FilterOption)
- `selectedDifficulty` - выбранная сложность (FilterOption)
- `selectedOrdering` - выбранная сортировка (FilterOption)
- `currentPage` - текущая страница
- `apiFilters` - параметры для API запроса (CourseFilters)

**Методы**:

- `updateSearch(value)` - обновить поиск
- `updateCategory(option)` - обновить категорию
- `updateDifficulty(option)` - обновить сложность
- `updateOrdering(option)` - обновить сортировку
- `updatePage(page)` - обновить страницу (без сброса на 1)
- `applyFilters(filters)` - применить несколько фильтров одновременно
- `resetFilters()` - сбросить все фильтры

**Пример использования**:

```typescript
import {
  COURSE_PAGE_SIZE_DEFAULT,
  COURSE_ORDERING_DEFAULT,
} from "~/constants/courseFilters";

const {
  searchValue,
  selectedCategory,
  currentPage,
  apiFilters,
  applyFilters,
  resetFilters,
  updatePage,
} = useCourseFilters(categoryOptions, difficultyOptions, orderingOptions, {
  pageSize: COURSE_PAGE_SIZE_DEFAULT,
  defaultOrdering: COURSE_ORDERING_DEFAULT,
});

// Применение фильтров пакетом
function handleApplyFilters(filters) {
  applyFilters(filters);
}

// Использование в getCourses
const { data, refresh } = await getCourses(apiFilters.value);

// Автоматический рефетч при изменении фильтров
watch(
  apiFilters,
  async () => {
    await refresh();
  },
  { deep: true }
);
```

**Особенности работы с URL**:

- Все фильтры синхронизируются с query параметрами URL
- При изменении фильтров (кроме страницы) пагинация сбрасывается на 1
- `applyFilters()` обновляет несколько параметров атомарно
- Изменения URL автоматически триггерят рефетч через watch на `apiFilters`
- `searchValue` - текущее значение поиска
- `selectedCategory` - выбранная категория (FilterOption)
- `selectedDifficulty` - выбранная сложность (FilterOption)
- `selectedOrdering` - выбранная сортировка (FilterOption)
- `currentPage` - текущая страница
- `apiFilters` - параметры для API запроса (CourseFilters)

**Методы**:

- `updateSearch(value)` - обновить поиск
- `updateCategory(option)` - обновить категорию
- `updateDifficulty(option)` - обновить сложность
- `updateOrdering(option)` - обновить сортировку
- `updatePage(page)` - обновить страницу
- `resetFilters()` - сбросить все фильтры

**Пример использования**:

```typescript
const {
  searchValue,
  selectedCategory,
  currentPage,
  apiFilters,
  updateSearch,
  updateCategory,
  updatePage,
} = useCourseFilters(categoryOptions, difficultyOptions, orderingOptions, {
  pageSize: 12,
  defaultOrdering: "-created_at",
});

// Использование в getCourses
const { data } = await getCourses(apiFilters.value);
```

## Best Practices

1. **Single Responsibility**: Каждый компонент отвечает за одну задачу
2. **Props типизация**: Все props строго типизированы
3. **Emit события**: Используются типизированные события для связи компонентов
4. **Computed свойства**: Для производных данных (badges, форматирование)
5. **Composables**: Бизнес-логика вынесена в composables
6. **UX**: Правильная обработка состояний загрузки, ошибок и пустых результатов
