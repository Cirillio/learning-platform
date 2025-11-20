# Анализ работы пагинации и запросов курсов

## 📋 Обзор

Django REST Framework автоматически обрабатывает пагинацию для всех ViewSet'ов, используя глобальные настройки из `settings.py`.

## ⚙️ Настройки пагинации (settings.py)

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,  # Размер страницы по умолчанию
}
```

### Параметры:

- **DEFAULT_PAGINATION_CLASS**: `PageNumberPagination` - стандартный класс пагинации DRF
- **PAGE_SIZE**: `20` - количество элементов на странице по умолчанию

## 🔍 Как работают запросы курсов

### 1. CourseViewSet (courses/views.py)

```python
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['created_at', 'title', 'difficulty']
```

### 2. Доступные фильтры

#### GET параметры:

- **search** - поиск по полям: `title`, `description`, `short_description`
- **category** - фильтрация по slug категории
- **difficulty** - фильтрация по уровню сложности (`beginner`, `intermediate`, `advanced`)
- **status** - фильтрация по статусу (`draft`, `published`, `archived`)
- **ordering** - сортировка по полям: `created_at`, `title`, `difficulty`
- **page** - номер страницы (для пагинации)
- **page_size** - размер страницы (переопределяет PAGE_SIZE)

#### Примеры запросов:

```bash
# Все опубликованные курсы, страница 1
GET /api/courses/?status=published&page=1

# Поиск курсов по Python, сортировка по дате
GET /api/courses/?search=python&ordering=-created_at

# Курсы категории "programming", уровень "beginner", 12 на странице
GET /api/courses/?category=programming&difficulty=beginner&page_size=12

# Курсы, отсортированные по названию, страница 2
GET /api/courses/?ordering=title&page=2
```

## 📊 Формат ответа с пагинацией

Django REST Framework автоматически оборачивает результаты в формат:

```json
{
  "count": 45, // Общее количество элементов
  "next": "http://api.example.com/courses/?page=3", // URL следующей страницы
  "previous": "http://api.example.com/courses/?page=1", // URL предыдущей страницы
  "results": [
    // Массив курсов
    {
      "id": 1,
      "title": "Python для начинающих",
      "slug": "python-for-beginners",
      "short_description": "...",
      "teacher": 2,
      "teacher_name": "Иван Иванов",
      "category": 1,
      "category_name": "Программирование",
      "cover_image": "/media/course_covers/python.jpg",
      "cover_image_url": "/media/course_covers/python.jpg",
      "status": "published",
      "difficulty": "beginner",
      "duration_weeks": 8,
      "max_students": 30,
      "enrolled_count": 15,
      "is_featured": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T14:20:00Z"
    }
    // ... остальные курсы
  ]
}
```

## 🔧 Логика фильтрации в get_queryset()

```python
def get_queryset(self):
    queryset = super().get_queryset()

    # 1. Фильтр по категории
    category = self.request.query_params.get('category', None)
    if category:
        queryset = queryset.filter(category__slug=category)

    # 2. Фильтр по сложности
    difficulty = self.request.query_params.get('difficulty', None)
    if difficulty:
        queryset = queryset.filter(difficulty=difficulty)

    # 3. Фильтр по статусу
    status_filter = self.request.query_params.get('status', None)
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    # 4. Права доступа: студенты видят только опубликованные курсы
    #    (кроме тех, на которые записаны)
    if self.request.user.is_authenticated and self.request.user.role == 'student':
        enrolled_courses = self.request.user.course_enrollments.filter(
            is_active=True
        ).values_list('course_id', flat=True)
        queryset = queryset.filter(
            Q(status='published') | Q(id__in=enrolled_courses)
        )

    # 5. Оптимизация запросов + подсчет записавшихся
    return queryset.select_related('teacher', 'category').annotate(
        enrollments_count=Count('enrollments', filter=Q(enrollments__is_active=True))
    )
```

### Особенности:

1. **select_related** - предзагрузка связанных объектов (teacher, category) одним запросом
2. **annotate** - подсчет количества активных записей через `enrollments_count`
3. **Права доступа** - автоматическая фильтрация по роли пользователя

## 🎯 Эндпоинт опций фильтров

### CourseFilterOptionsView

```python
GET /api/courses/filters/
```

Возвращает все доступные значения для фильтров:

```json
{
  "filters": [
    {
      "value": "difficulty",
      "label": "Сложность",
      "values": [
        { "value": "beginner", "label": "Начальный" },
        { "value": "intermediate", "label": "Средний" },
        { "value": "advanced", "label": "Продвинутый" }
      ]
    },
    {
      "value": "status",
      "label": "Статус",
      "values": [
        { "value": "draft", "label": "Черновик" },
        { "value": "published", "label": "Опубликован" },
        { "value": "archived", "label": "Архивирован" }
      ]
    },
    {
      "value": "ordering",
      "label": "Сортировка",
      "values": [
        { "value": "created_at", "label": "По дате создания (сначала старые)" },
        { "value": "-created_at", "label": "По дате создания (сначала новые)" },
        { "value": "title", "label": "По названию (А-Я)" },
        { "value": "-title", "label": "По названию (Я-А)" }
      ]
    },
    {
      "value": "category",
      "label": "Категория",
      "values": [
        { "value": "programming", "label": "Программирование" },
        { "value": "design", "label": "Дизайн" }
      ]
    }
  ]
}
```

## 🚀 Как работает пагинация

### 1. Автоматическая пагинация

DRF автоматически применяет пагинацию ко всем ViewSet'ам:

- Читает параметр `?page=N` из query string
- Опционально читает `?page_size=N` для изменения размера страницы
- Возвращает срез данных с метаданными (count, next, previous)

### 2. Вычисление страниц

```python
# Формула расчета количества страниц:
total_pages = ceil(count / page_size)

# Пример:
# count = 45, page_size = 20
# total_pages = ceil(45 / 20) = 3 страницы
```

### 3. Навигация

- **next**: URL следующей страницы (null если это последняя)
- **previous**: URL предыдущей страницы (null если это первая)
- **count**: общее количество элементов (для вычисления кол-ва страниц)

## 💡 Интеграция с фронтендом (Nuxt)

### useCourses composable

```typescript
interface CourseFilters {
  category?: string;
  difficulty?: string;
  status?: string;
  search?: string;
  ordering?: string;
  page?: number; // Номер страницы
  page_size?: number; // Размер страницы
}

const getCourses = (params: CourseFilters) => {
  return useAsyncData<CoursesResponse>(
    // Уникальный ключ для кеширования
    `courses-${JSON.stringify(params)}`,
    () =>
      api("/courses/", {
        method: "GET",
        params: {
          // Отправляем только заполненные параметры
          ...(params.search ? { search: params.search } : {}),
          ...(params.category ? { category: params.category } : {}),
          ...(params.difficulty ? { difficulty: params.difficulty } : {}),
          ...(params.ordering ? { ordering: params.ordering } : {}),
          ...(params.page ? { page: params.page } : {}),
          ...(params.page_size ? { page_size: params.page_size } : {}),
        },
      }),
    {
      // Автоматическая перезагрузка при изменении параметров
      watch: [
        () => params.search,
        () => params.category,
        () => params.difficulty,
        () => params.ordering,
        () => params.page,
      ],
    }
  );
};
```

### Использование на странице

```vue
<script setup>
const PAGE_SIZE = 12; // Переопределяем размер страницы

const filters = computed(() => ({
  search: String(route.query.search || ""),
  category: String(route.query.category || ""),
  difficulty: String(route.query.difficulty || ""),
  ordering: String(route.query.ordering || "-created_at"),
  page: Number(route.query.page || 1),
  page_size: PAGE_SIZE,
}));

const { data: coursesResponse } = await getCourses(filters.value);

const currentPage = computed(() => filters.value.page);
const totalItems = computed(() => coursesResponse.value?.count || 0);
const courses = computed(() => coursesResponse.value?.results || []);
</script>

<template>
  <UPagination
    :page="currentPage"
    :total="totalItems"
    :items-per-page="PAGE_SIZE"
    @update:page="updatePage"
  />
</template>
```

## 🎨 Преимущества текущей реализации

✅ **Автоматическая пагинация** - не нужно вручную реализовывать логику  
✅ **Гибкость** - можно переопределить `page_size` для разных страниц  
✅ **SEO-friendly** - пагинация через URL параметры  
✅ **SSR поддержка** - работает с server-side rendering  
✅ **Оптимизация** - select_related и annotate для минимизации запросов  
✅ **Безопасность** - автоматическая фильтрация по правам доступа

## 📌 Важные моменты

1. **Размер страницы по умолчанию**: 20 элементов (можно переопределить через `page_size`)
2. **Нумерация страниц**: начинается с 1, а не с 0
3. **Фильтры сохраняются**: при переходе между страницами все фильтры остаются
4. **Кеширование**: Nuxt кеширует результаты по ключу с параметрами
5. **Автообновление**: изменение любого фильтра сбрасывает страницу на 1

## 🔗 URL структура

```
# Примеры финальных URL:
/courses/all?search=python&page=1
/courses/all?category=programming&difficulty=beginner&page=2
/courses/all?ordering=-created_at&page=3&page_size=12
```

Все параметры синхронизированы с адресной строкой браузера, что позволяет:

- Делиться ссылками на отфильтрованные списки
- Использовать кнопки браузера "назад/вперед"
- Сохранять состояние при перезагрузке страницы
