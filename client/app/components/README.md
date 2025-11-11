# Компоненты приложения

## Структура папок

```
components/
├── app/                    # Общие компоненты приложения
│   └── logo.vue           # Логотип приложения
├── header/                 # Компоненты шапки
│   ├── auth/              # Компоненты аутентификации
│   │   └── actions-desktop.vue
│   └── navigation/        # Навигационные компоненты
│       └── menu-desktop.vue
├── layout/                 # Компоненты layout'а
│   ├── header.vue         # Только шапка сайта (UHeader)
│   ├── main.vue           # Основная область контента (UMain + UContainer)
│   └── footer.vue         # Только подвал сайта (UFooter)
└── sections/               # Секции страниц
    ├── hero.vue           # Hero секция
    ├── features.vue       # Секция преимуществ
    ├── testimonials.vue   # Секция отзывов
    └── cta.vue           # Призыв к действию
```

## Соглашения по именованию

- **Файлы компонентов**: `kebab-case.vue` (component-name.vue)
- **Импорты в шаблонах**: `PascalCase` (ComponentName)
- **Папки**: `kebab-case` или описательные имена

## Типы компонентов

### Layout компоненты

Отвечают за общую структуру страницы:

- `LayoutHeader` - шапка сайта
- `LayoutMain` - основная область
- `LayoutFooter` - подвал сайта

### Section компоненты

Отдельные секции страниц:

- `SectionsHero` - приветственная секция
- `SectionsFeatures` - преимущества
- `SectionsTestimonials` - отзывы
- `SectionsCta` - призыв к действию

### App компоненты

Общие компоненты приложения:

- `AppLogo` - логотип

### Header компоненты

Компоненты шапки сайта:

- `HeaderNavigationMenuDesktop` - навигационное меню
- `HeaderAuthActionsDesktop` - действия аутентификации
