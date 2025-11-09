# Django Backend - Quick Start

## Шаг 3: Модели - ВЫПОЛНЕНО ✅

Все модели созданы, миграции применены, admin настроен!

## Быстрый старт

### 1. Активация виртуального окружения

```bash
cd /home/cirillio/web/javascript/NUXT/University/server
source virtenv/bin/activate
```

### 2. Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите данные:

- Username: admin
- Email: admin@example.com
- Password: (ваш пароль)

### 3. Заполнение тестовыми данными (опционально)

```bash
python manage.py seed_data
```

Это создаст:

- 2 преподавателя: teacher1, teacher2
- 3 студента: student1, student2, student3
- 3 курса с уроками и заданиями
- Тестовые оценки, комментарии, уведомления

**Пароль для всех**: `password123`

### 4. Запуск сервера

```bash
python manage.py runserver
```

### 5. Открыть админку

Откройте в браузере: http://127.0.0.1:8000/admin/

Войдите с учетными данными суперпользователя.

## Что доступно в админке

### Пользователи

- **Users** - все пользователи с ролями
- **User Profiles** - расширенные профили

### Курсы

- **Categories** - категории курсов
- **Courses** - курсы с inline уроками
- **Course Enrollments** - записи студентов
- **Lessons** - уроки с inline материалами и заданиями
- **Lesson Materials** - файлы уроков
- **Assignments** - задания
- **Assignment Files** - файлы заданий
- **Submissions** - ответы студентов
- **Submission Files** - файлы ответов
- **Grades** - оценки

### Взаимодействие

- **Comments** - комментарии
- **Notifications** - уведомления (с действиями mark as read/unread)
- **Feedbacks** - обратная связь
- **Activity Logs** - журнал активности

## Структура моделей

Подробнее в файлах:

- **MODELS_README.md** - описание всех моделей
- **USAGE_GUIDE.md** - примеры использования
- **STEP_3_COMPLETE.md** - полный отчет

## Полезные команды

### Проверка системы

```bash
python manage.py check
```

### Django shell (интерактивная консоль)

```bash
python manage.py shell
```

Примеры в shell:

```python
# Все курсы
from courses.models import Course
Course.objects.all()

# Все студенты
from users.models import User
User.objects.filter(role='student')

# Уроки курса
course = Course.objects.first()
course.lessons.all()
```

### Миграции (если нужно)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание новых миграций после изменений

```bash
python manage.py makemigrations
python manage.py migrate
```

## Следующий шаг

**Шаг 4: Создание сериализаторов DRF**

Готовы создавать API endpoints!

## Проблемы?

### Ошибка импорта

```bash
python manage.py check
```

### База данных заблокирована

Остановите сервер и попробуйте снова

### Забыли пароль суперпользователя

```bash
python manage.py changepassword admin
```

## Документация

1. **MODELS_README.md** - все модели с описанием полей
2. **USAGE_GUIDE.md** - примеры кода для работы с моделями
3. **STEP_3_COMPLETE.md** - детальный отчет о шаге 3
4. **SUMMARY_STEP_3.md** - краткая сводка

---

**Статус**: Шаг 3 полностью завершен! ✅
**Готово к**: Разработке API (сериализаторы, views, endpoints)
