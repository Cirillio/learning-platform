# Скелетоны загрузки

Компоненты скелетонов используются для улучшения пользовательского опыта во время загрузки контента.

## Компоненты

### SkeletonsHomePage

Полноэкранный скелетон для главной страницы, имитирующий все секции:

- Hero секция с заголовком, описанием и изображением
- Features секция с карточками преимуществ
- Testimonials секция с отзывами
- CTA секция с кнопками и статистикой

```vue
<template>
  <Suspense>
    <HomePageContent />
    <template #fallback>
      <SkeletonsHomePage />
    </template>
  </Suspense>
</template>
```

### UiContentSkeleton

Универсальный компонент для создания скелетонов контента.

#### Props

- `lines` (number, default: 3) - количество строк текста
- `lineHeight` ('sm' | 'md' | 'lg', default: 'md') - высота строк
- `showAvatar` (boolean, default: false) - показать аватар
- `showAction` (boolean, default: false) - показать кнопку действия
- `lastLineWidth` (string, default: '4/6') - ширина последней строки

#### Примеры использования

```vue
<!-- Простой текстовый контент -->
<UiContentSkeleton />

<!-- Контент с аватаром -->
<UiContentSkeleton :show-avatar="true" />

<!-- Комментарий с кнопкой действия -->
<UiContentSkeleton :lines="2" :show-action="true" />

<!-- Большой заголовок -->
<UiContentSkeleton :lines="1" :line-height="'lg'" />
```

## Использование в Nuxt 3

### С компонентом Suspense (рекомендуемый подход)

```vue
<!-- pages/index.vue -->
<template>
  <Suspense>
    <HomePageContent />
    <template #fallback>
      <SkeletonsHomePage />
    </template>
  </Suspense>
</template>
```

```vue
<!-- components/home-page-content.vue -->
<template>
  <div>
    <SectionsHero />
    <SectionsFeatures />
    <!-- другие секции -->
  </div>
</template>
```

### С defineAsyncComponent

Для более сложных случаев с ленивой загрузкой:

```ts
// В роутере или компоненте
import { defineAsyncComponent } from "vue";

const HomePage = defineAsyncComponent({
  loader: () => import("@/pages/HomePage.vue"),
  loadingComponent: SkeletonsHomePage,
  delay: 200, // Задержка перед показом скелетона
  timeout: 10000, // Таймаут загрузки
});
```

### С динамическими импортами

```vue
<script setup>
const HomePageContent = defineAsyncComponent(() =>
  import("@/components/HomePageContent.vue")
);
</script>

<template>
  <Suspense>
    <HomePageContent />
    <template #fallback>
      <SkeletonsHomePage />
    </template>
  </Suspense>
</template>
```

## Лучшие практики

1. **Suspense для страниц**: Используйте `<Suspense>` для целых страниц или больших компонентов
2. **defineAsyncComponent для роутов**: Используйте для ленивой загрузки маршрутов
3. **Время загрузки**: Скелетон должен показываться не дольше 2-3 секунд
4. **Структура**: Скелетон должен точно имитировать структуру реального контента
5. **Анимации**: Используйте плавные анимации появления для лучшего UX
6. **Цвета**: Используйте нейтральные цвета, соответствующие теме приложения
7. **Размеры**: Скелетон должен занимать то же пространство, что и реальный контент

## Примеры из проекта

Главная страница использует `<Suspense>` с `SkeletonsHomePage` в качестве fallback компонента, что обеспечивает плавную загрузку всех секций страницы.
