# Реализация системы комментариев к урокам

## Описание задачи
Необходимо реализовать полную систему комментариев к урокам на фронтенде. Бэкенд уже поддерживает комментарии через модель Comment с Generic Foreign Key, но фронтенд требует полной реализации UI и логики.

**Документация Nuxt UI**: `/docs/nuxt-ui-components/`  
**Золотой стандарт верстки**: Страницы учителя (`/teacher/`), особенно компоненты в `/components/teacher/profile/`

## Требования к функциональности

### Основные возможности
- **Просмотр комментариев** к уроку
- **Добавление новых комментариев** (студенты и преподаватели)
- **Ответы на комментарии** (вложенная структура)
- **Отображение роли автора** (учитель/студент) с визуальными индикаторами
- **Редактирование собственных комментариев** (только автор)
- **Удаление собственных комментариев** (только автор)

### UI/UX требования
- **Четкое разделение ролей**: комментарии преподавателей выделены (фон, иконка, цвет)
- **Вложенная структура**: отступы для ответов, максимум 3 уровня вложенности
- **Реал-тайм обновления**: optimistic updates при добавлении
- **Адаптивный дизайн**: корректное отображение на мобильных
- **Индикаторы состояния**: loading, error states
- **Пагинация**: для большого количества комментариев

### Безопасность и валидация
- **Zod схемы** для валидации комментариев
- **Проверка прав**: только автор может редактировать/удалять
- **Санитизация контента**: защита от XSS
- **Rate limiting**: защита от спама (если потребуется)

## Технические детали

### API Endpoints (уже реализованы)
```
GET    /api/core/comments/?content_type=<lesson_type>&object_id=<lesson_id>
POST   /api/core/comments/ - создание комментария
PUT    /api/core/comments/<id>/ - обновление
DELETE /api/core/comments/<id>/ - удаление
```

### Модель данных
```typescript
interface Comment {
  id: number;
  content_type: number; // ContentType ID для Lesson
  object_id: number;   // ID урока
  author: {
    id: number;
    username: string;
    profile: {
      role: 'student' | 'teacher';
      avatar?: string;
    }
  };
  text: string;
  parent?: number;     // ID родительского комментария
  created_at: string;
  updated_at: string;
  is_edited: boolean;
  replies_count: number;
}
```

## Шаги реализации

### 1. Создание composable `useComments.ts`
- API функции для CRUD операций
- Reactive состояние комментариев
- Обработка ошибок и loading states
- Optimistic updates
- Функции для работы с вложенностью

### 2. Создание схем валидации `comment.schema.ts`
- Zod схема для создания комментария
- Схема для обновления
- Валидация длины текста (минимум 1, максимум 1000 символов)

### 3. Создание компонентов

#### `CommentList.vue`
- Отображение списка комментариев
- Рекурсивное отображение ответов
- Индикаторы ролей (badge для преподавателей)
- Кнопки действий (ответить, редактировать, удалить)

#### `CommentForm.vue`
- Форма для нового комментария или ответа
- WYSIWYG редактор (опционально, простой textarea)
- Валидация в реальном времени
- Отправка с optimistic update

#### `CommentItem.vue`
- Отдельный комментарий с ответами
- Аватар автора, имя, роль, время
- Текст комментария
- Действия (если автор текущий пользователь)

### 4. Интеграция в страницу урока
- Добавить секцию комментариев в `[lesson_slug].vue`
- Загрузка комментариев при открытии урока
- Обновление при навигации между уроками

### 5. Стилизация и анимации
- Использование Tailwind CSS
- Плавные переходы при добавлении/удалении
- Hover эффекты для интерактивности
- Темная тема поддержка

## Nuxt UI компоненты для реализации

### Основные компоненты (документация в `/docs/nuxt-ui-components/`)

#### `UCard` - Контейнер для комментариев
```vue
<UCard class="mb-4">
  <!-- Содержимое комментария -->
</UCard>
```

#### `UAvatar` - Аватар пользователя
```vue
<UAvatar
  :src="comment.author.avatar"
  :alt="comment.author.name"
  size="sm"
/>
```

#### `UBadge` - Индикатор роли (золотой стандарт из страниц учителя)
```vue
<!-- Для преподавателей -->
<UBadge color="primary" variant="subtle" size="sm">
  <UIcon name="i-lucide-graduation-cap" class="size-3" />
  Преподаватель
</UBadge>

<!-- Для студентов -->
<UBadge color="neutral" variant="outline" size="sm">
  Студент
</UBadge>
```

#### `UButton` - Кнопки действий
```vue
<UButton
  size="xs"
  variant="ghost"
  icon="i-lucide-message-circle"
  @click="replyToComment"
>
  Ответить
</UButton>
```

#### `UTextarea` - Форма комментария
```vue
<UTextarea
  v-model="commentText"
  placeholder="Напишите комментарий..."
  rows="3"
  maxlength="1000"
/>
```

#### `USkeleton` - Загрузка комментариев
```vue
<USkeleton class="h-20 w-full rounded-lg mb-4" />
```

#### `UAlert` - Сообщения об ошибках
```vue
<UAlert
  v-if="error"
  color="error"
  variant="outline"
  title="Ошибка загрузки комментариев"
  :description="error.message"
/>
```

### Стиль верстки (золотой стандарт - страницы учителя)

#### Структура компонентов
- Использовать `UCard` как основной контейнер (как в `TeacherProfileHeaderCard.vue`)
- Аватар слева, контент справа с `flex` layout
- Роли выделять `UBadge` с иконками (как в профиле преподавателя)
- Кнопки действий в `justify-between` или `justify-end` flex

#### Цветовая схема
- Преподаватели: `color="primary"` с `variant="subtle"`
- Студенты: `color="neutral"` с `variant="outline"`
- Акцентные элементы: `color="primary"`

#### Размеры и отступы
- Аватары: `size="sm"` (32px) или `size="xs"` (24px)
- Badge: `size="sm"`
- Кнопки: `size="xs"` для второстепенных действий
- Отступы: `gap-2`, `gap-3` для spacing

#### Адаптивность
- На мобильных: `flex-col` вместо `flex-row`
- Аватар всегда сверху или слева
- Текст переносится корректно

### Рекомендуемые паттерны

#### Комментарий преподавателя (выделенный)
```vue
<UCard class="border-primary/20 bg-primary/5">
  <div class="flex gap-3">
    <UAvatar :src="author.avatar" size="sm" class="ring-2 ring-primary/50" />
    <div class="flex-1">
      <div class="flex items-center gap-2 mb-2">
        <span class="font-medium">{{ author.name }}</span>
        <UBadge color="primary" variant="subtle" size="sm">
          <UIcon name="i-lucide-graduation-cap" class="size-3" />
          Преподаватель
        </UBadge>
      </div>
      <p class="text-sm">{{ comment.text }}</p>
    </div>
  </div>
</UCard>
```

#### Комментарий студента (стандартный)
```vue
<UCard>
  <div class="flex gap-3">
    <UAvatar :src="author.avatar" size="sm" />
    <div class="flex-1">
      <div class="flex items-center gap-2 mb-2">
        <span class="font-medium">{{ author.name }}</span>
        <UBadge color="neutral" variant="outline" size="sm">
          Студент
        </UBadge>
      </div>
      <p class="text-sm">{{ comment.text }}</p>
    </div>
  </div>
</UCard>
```

#### Вложенные комментарии (с отступами)
```vue
<!-- Родительский комментарий -->
<UCard class="mb-3">
  <!-- контент -->
</UCard>

<!-- Ответ (с отступом) -->
<div class="ml-8 border-l-2 border-muted pl-4">
  <UCard class="mb-3">
    <!-- контент ответа -->
  </UCard>
</div>
```

## Пометка про бэкенд
Бэкенд уже полностью реализован и поддерживает все необходимые операции. При необходимости можно обновить модели или API (например, добавить модерацию, лайки или дополнительные поля), но текущая реализация достаточна для MVP.

## Критерии приемки
- [ ] Студент может оставлять комментарии к уроку
- [ ] Преподаватель может оставлять комментарии к уроку
- [ ] Комментарии преподавателей визуально выделены
- [ ] Можно отвечать на комментарии (вложенная структура)
- [ ] Автор может редактировать свои комментарии
- [ ] Автор может удалять свои комментарии
- [ ] Комментарии загружаются при открытии урока
- [ ] UI адаптивен и соответствует дизайну
- [ ] Обработка ошибок и loading states
- [ ] Валидация форм на фронтенде
- [ ] Использованы компоненты Nuxt UI согласно документации
- [ ] Стиль верстки соответствует золотому стандарту страниц учителя