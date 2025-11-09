# Быстрый старт Backend API

## Предварительные требования

- Python 3.10+
- Redis (для Celery)
- SQLite (уже в Python)

## Установка и запуск

### 1. Активация виртуального окружения

```bash
cd server
source virtenv/bin/activate  # Linux/Mac
# или
virtenv\Scripts\activate  # Windows
```

### 2. Применение миграций

```bash
python manage.py migrate
```

### 3. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 4. Загрузка тестовых данных (опционально)

```bash
python manage.py seed_data
```

### 5. Запуск Django сервера

```bash
python manage.py runserver
```

Django будет доступен по адресу: `http://localhost:8000`

### 6. Запуск Celery Worker (в отдельном терминале)

```bash
# Активируйте виртуальное окружение
source virtenv/bin/activate

# Запустите worker
celery -A config worker -l info
```

### 7. Запуск Celery Beat (в третьем терминале, опционально)

```bash
# Активируйте виртуальное окружение
source virtenv/bin/activate

# Запустите beat scheduler
celery -A config beat -l info
```

**Альтернатива:** запустить worker и beat вместе:

```bash
celery -A config worker -B -l info
```

## Доступные эндпоинты

### Аутентификация

- `POST /api/auth/register/` - Регистрация
- `POST /api/token/` - Получить JWT токен
- `POST /api/token/refresh/` - Обновить токен
- `GET /api/auth/profile/` - Профиль
- `GET /api/users/me/` - Текущий пользователь

### Курсы

- `GET /api/courses/` - Список курсов
- `POST /api/courses/` - Создать курс (teacher)
- `POST /api/courses/{slug}/enroll/` - Записаться на курс (student)
- `GET /api/courses/my_courses/` - Мои курсы

### Задания и ответы

- `GET /api/assignments/` - Список заданий
- `POST /api/submissions/` - Отправить ответ (student)
- `POST /api/grades/` - Выставить оценку (teacher)

### Уведомления

- `GET /api/notifications/` - Список уведомлений
- `POST /api/notifications/{id}/mark_as_read/` - Пометить как прочитанное
- `GET /api/notifications/unread_count/` - Количество непрочитанных

### Комментарии

- `GET /api/comments/` - Список комментариев
- `POST /api/comments/` - Создать комментарий

### Админка

- `http://localhost:8000/admin/` - Django Admin Panel

## Примеры запросов

### Регистрация студента

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "email": "student@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "role": "student",
    "first_name": "Иван",
    "last_name": "Иванов",
    "student_id": "ST-2024-001",
    "enrollment_year": 2024
  }'
```

### Получение токена

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "securepass123"
  }'
```

### Использование токена

```bash
curl -X GET http://localhost:8000/api/courses/ \
  -H "Authorization: Bearer <ваш_access_token>"
```

## Проверка Celery

### Проверить, что Redis работает:

```bash
redis-cli ping
# Должен вернуть: PONG
```

### Тестовая задача:

```python
# В Django shell
python manage.py shell

from config.celery import debug_task
result = debug_task.delay()
print(result.get())
```

## Структура проекта

```
server/
├── config/              # Основные настройки
│   ├── settings.py     # Django настройки
│   ├── urls.py         # Главный URL роутинг
│   └── celery.py       # Celery конфигурация
├── users/              # Пользователи и аутентификация
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── courses/            # Курсы, уроки, задания
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tasks.py        # Celery задачи
├── notifications/      # Уведомления
│   ├── models.py
│   ├── views.py
│   └── tasks.py
├── core/               # Общие модели (комментарии, feedback)
│   ├── models.py
│   ├── views.py
│   └── tasks.py
└── manage.py
```

## Troubleshooting

### Redis не запускается

```bash
# Установить Redis (Ubuntu/Debian)
sudo apt-get install redis-server

# Запустить Redis
redis-server

# Проверить статус
redis-cli ping
```

### Ошибки миграций

```bash
# Удалить все миграции и создать заново
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

### Celery не видит tasks

```bash
# Убедитесь, что в каждом приложении есть tasks.py
# Перезапустите Celery worker
```

## Полезные команды

```bash
# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить shell
python manage.py shell

# Собрать статику
python manage.py collectstatic

# Проверить настройки
python manage.py check

# Просмотр всех URL
python manage.py show_urls  # требует django-extensions
```

## Следующие шаги

1. ✅ Настроить Email (SMTP)
2. ✅ Протестировать API endpoints
3. ✅ Добавить API документацию (drf-spectacular)
4. ✅ Написать тесты
5. ✅ Настроить production окружение
