# Разработка бэкенда

## Запуск

Python 3.12, Redis обязателен: вход ставит Celery-задачу, и без брокера запрос логина зависает.

```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine

cd server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "REDIS_URL=redis://localhost:6379/0" >> .env
python manage.py migrate
python manage.py seed_data          # демо-данные
python manage.py runserver          # http://localhost:8000

celery -A config worker -l info     # по желанию, отдельные терминалы
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Через Docker Compose из корня: `docker compose up -d --build`, команды — `make help`.

## Демо-данные

| Команда | Что делает |
| :--- | :--- |
| `python manage.py seed_data` | Преподаватели `teacher1`, `teacher2`, студенты `student1`–`student3` (пароль `password123`), категории, курсы, уроки, задания, ответы, оценки, уведомления. Идемпотентна (`get_or_create`). |
| `python manage.py seed_db [--clear]` | Расширенный набор: много курсов и студентов `teststudent1…` (пароль `testpass123`). `--clear` удаляет курсы, уроки, задания, ответы и оценки перед заполнением. |
| `python manage.py dumpdata_to_json` | Выгрузка всех моделей в JSON (собственный формат, не фикстура для `loaddata`). Результат не коммитить: в нём персональные данные. |

Администратор: `python manage.py createsuperuser`, панель — http://localhost:8000/admin/.
Роль `teacher` можно назначить пользователю там же.

## Переменные окружения (`server/.env`)

| Переменная | По умолчанию | Назначение |
| :--- | :--- | :--- |
| `DJANGO_SECRET_KEY` | dev-ключ | Секрет Django. В проде — обязательно свой. |
| `DEBUG` | `True` | Режим отладки. |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Разрешённые хосты. |
| `REDIS_URL` | `redis://redis:6379/0` | Брокер и backend Celery. Локально — `redis://localhost:6379/0`. |
| `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` | SMTP Gmail | Письма-уведомления. Для разработки удобно `django.core.mail.backends.console.EmailBackend` или Mailhog из docker-compose. |

## Тесты

```bash
python manage.py test                 # все приложения
python manage.py test courses         # одно приложение
```

Тесты лежат в `<app>/tests.py` и `<app>/test_serializers.py`.

## Полезное в `python manage.py shell`

```python
from users.models import User
from courses.models import Course, CourseEnrollment, Submission

# Курсы преподавателя
Course.objects.filter(teacher__username="teacher1", status="published")

# Прогресс студента по курсам
for e in CourseEnrollment.objects.filter(student__username="student1", is_active=True):
    print(e.course.title, e.progress)

# Работы, ожидающие проверки
Submission.objects.filter(status="pending").select_related("assignment", "student")

# Непрочитанные уведомления
User.objects.get(username="student1").notifications.filter(is_read=False).count()
```

## Миграции

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations      # что применено
```

После изменения моделей — проверить `admin.py` и сериализаторы соответствующего приложения.
