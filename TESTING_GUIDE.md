# Руководство по тестированию API учебного портала

Данный документ содержит инструкции по тестированию функционала учебного портала через его API в **Insomnia** или **Postman**.
Для каждой функции представлены эндпоинты, методы запроса, необходимые данные и примеры использования.

**Базовая настройка:**

- **Base URL:** `http://localhost:8000/api` (или ваш сервер)
- **Authorization:** Bearer Token (получается после логина)
- Замените все `<PLACEHOLDER>` значения на актуальные данные из вашей системы.

---

## 1. Аутентификация и Управление Пользователями

### 1.1. Регистрация пользователя (Student)

**Метод:** `POST`
**URL:** `/auth/register/`
**Headers:**

```
Content-Type: application/json
```

**Body (JSON):**

```json
{
  "email": "student@example.com",
  "username": "student_user",
  "first_name": "Иван",
  "last_name": "Петров",
  "password": "strong_password",
  "password_confirm": "strong_password",
  "remember_me": false
}
```

**Примечание:** Поле `role` не требуется - по умолчанию создается студент. Поля `first_name` и `last_name` обязательны. Поле `remember_me` влияет на время жизни токенов (30 дней если `true`, 7 дней если `false`).

**Пример ответа (201 Created):**

```json
{
  "user": {
    "id": 1,
    "email": "student@example.com",
    "username": "student_user",
    "first_name": "Иван",
    "last_name": "Петров",
    "role": "student",
    "date_joined": "2025-11-24T10:00:00Z"
  }
}
```

**Важно:** После регистрации токены устанавливаются в httpOnly cookies автоматически (`access_token`, `refresh_token`).

---

### 1.1.2. Регистрация пользователя (Teacher)

**Метод:** `POST`
**URL:** `/auth/register/`
**Headers:**

```
Content-Type: application/json
```

**Body (JSON):**

```json
{
  "email": "teacher@example.com",
  "username": "teacher_user",
  "first_name": "Мария",
  "last_name": "Иванова",
  "password": "strong_password",
  "password_confirm": "strong_password",
  "remember_me": true
}
```

**Примечание:** Для создания преподавателя нужно изменить роль через Django Admin или прямо в базе данных после регистрации. API не позволяет напрямую создавать преподавателей через публичную регистрацию.

**Пример ответа (201 Created):**

```json
{
  "user": {
    "id": 2,
    "email": "teacher@example.com",
    "username": "teacher_user",
    "first_name": "Мария",
    "last_name": "Иванова",
    "role": "student",
    "date_joined": "2025-11-24T10:05:00Z"
  }
}
```

---

### 1.2. Авторизация (Login)

**Метод:** `POST`
**URL:** `/auth/login/`
**Headers:**

```
Content-Type: application/json
```

**Body (JSON):**

```json
{
  "username": "student_user",
  "password": "strong_password",
  "remember_me": false
}
```

**Примечание:** Поле `remember_me` влияет на время жизни refresh токена (30 дней если `true`, 7 дней если `false`).

**Пример ответа (200 OK):**

```json
{
  "user": {
    "id": 1,
    "username": "student_user",
    "email": "student@example.com",
    "first_name": "Иван",
    "last_name": "Петров",
    "role": "student",
    "date_joined": "2025-11-24T10:00:00Z"
  }
}
```

**Важно:** Токены передаются через **httpOnly cookies** (`access_token`, `refresh_token`, `auth_remember_me`). В Insomnia/Postman они автоматически сохранятся. Для последующих запросов убедитесь, что включена опция "Send cookies automatically".

---

### 1.3. Обновление токена

**Метод:** `POST`
**URL:** `/auth/refresh/`
**Headers:**

```
Content-Type: application/json
```

**Authorization:** Требуется (refresh_token из cookies)

**Body:** Не требуется (refresh токен берется из cookies автоматически)

**Примечание:** Этот эндпоинт автоматически читает `refresh_token` из cookies и обновляет оба токена (`access_token` и `refresh_token`).

**Пример ответа (200 OK):**

```json
{
  "detail": "Token refreshed successfully"
}
```

**Важно:** Обновленные токены автоматически устанавливаются в cookies. Если refresh токен истек или невалиден, вернется ошибка 401.

---

### 1.4. Выход (Logout)

**Метод:** `POST`
**URL:** `/auth/logout/`
**Headers:**

```
Content-Type: application/json
```

**Authorization:** Требуется (cookies)

**Body:** Не требуется

**Пример ответа (200 OK):**

```json
{
  "detail": "Successfully logged out."
}
```

---

### 1.5. Просмотр профиля

**Метод:** `GET`
**URL:** `/auth/profile/`
**Authorization:** Требуется (cookies)

**Пример ответа (200 OK):**

```json
{
  "user": 1,
  "username": "student_user",
  "email": "student@example.com",
  "first_name": "Иван",
  "last_name": "Петров",
  "role": "student",
  "date_joined": "2025-11-24T10:00:00Z",
  "avatar": "http://localhost:8000/media/avatars/user_1.jpg",
  "bio": "Python разработчик",
  "phone": "+7 999 123-45-67",
  "birth_date": "1995-05-15",
  "address": "ул. Пушкина, д. 10",
  "city": "Москва",
  "country": "Россия",
  "specialization": "",
  "experience_years": null,
  "student_id": "STU001",
  "enrollment_year": 2024,
  "created_at": "2025-11-24T10:00:05Z",
  "updated_at": "2025-11-24T12:30:00Z"
}
```

**Примечание:** Поля `specialization` и `experience_years` заполняются для преподавателей. Поля `student_id` и `enrollment_year` - для студентов.

---

### 1.6. Редактирование профиля

**Метод:** `PATCH`
**URL:** `/auth/profile/`
**Headers:**

```
Content-Type: application/json
```

**Authorization:** Требуется (cookies)

**Body (JSON):**

```json
{
  "bio": "Senior Python Developer с 5-летним опытом",
  "first_name": "Иван",
  "last_name": "Петрович",
  "phone": "+7 999 888-77-66",
  "city": "Санкт-Петербург"
}
```

**Примечание:** Можно обновлять только нужные поля. Поля `username`, `email`, `role` доступны только для чтения. Поле `student_id` также только для чтения.

**Пример ответа (200 OK):**

```json
{
  "user": 1,
  "username": "student_user",
  "email": "student@example.com",
  "first_name": "Иван",
  "last_name": "Петрович",
  "role": "student",
  "date_joined": "2025-11-24T10:00:00Z",
  "avatar": "http://localhost:8000/media/avatars/user_1.jpg",
  "bio": "Senior Python Developer с 5-летним опытом",
  "phone": "+7 999 888-77-66",
  "birth_date": "1995-05-15",
  "address": "ул. Пушкина, д. 10",
  "city": "Санкт-Петербург",
  "country": "Россия",
  "specialization": "",
  "experience_years": null,
  "student_id": "STU001",
  "enrollment_year": 2024,
  "created_at": "2025-11-24T10:00:05Z",
  "updated_at": "2025-11-24T14:20:00Z"
}
```

---

## 2. Управление Курсами

### 2.1. Создание курса (только для преподавателей)

**Метод:** `POST`
**URL:** `/courses/`
**Headers:**

```
Content-Type: application/json
```

**Authorization:** Требуется (cookies, роль: teacher)

**Body (JSON):**

```json
{
  "title": "Основы Python",
  "slug": "osnovy-python",
  "description": "Полный курс по программированию на Python для начинающих. Изучите синтаксис, структуры данных, ООП и многое другое.",
  "short_description": "Базовый курс по программированию на Python",
  "category": 1,
  "difficulty": "beginner",
  "duration_weeks": 8,
  "max_students": 30,
  "status": "draft"
}
```

**Примечание:**

- Поле `teacher` устанавливается автоматически из текущего пользователя
- Поле `slug` опционально - если не указать, создастся автоматически из `title`
- `category` - это ID категории (можно получить из `/categories/`)
- `status` может быть: `draft`, `published`, `archived` (по умолчанию `draft`)
- `difficulty` может быть: `beginner`, `intermediate`, `advanced`

**Пример ответа (201 Created):**

```json
{
  "id": 1,
  "title": "Основы Python",
  "slug": "osnovy-python",
  "short_description": "Базовый курс по программированию на Python",
  "teacher": 2,
  "teacher_name": "Мария Иванова",
  "category": 1,
  "category_name": "Программирование",
  "cover_image": null,
  "cover_image_url": null,
  "status": "draft",
  "difficulty": "beginner",
  "duration_weeks": 8,
  "max_students": 30,
  "enrolled_count": 0,
  "is_featured": false,
  "created_at": "2025-11-24T10:30:00Z",
  "updated_at": "2025-11-24T10:30:00Z"
}
```

---

### 2.2. Просмотр всех курсов (с фильтрацией и сортировкой)

**Метод:** `GET`**URL:** `/courses/`**Query Parameters (опционально):**

- `category=<category_slug>` - фильтр по категории (используй **slug**, не ID)
- `difficulty=<beginner|intermediate|advanced>` - фильтр по сложности
- `status=<draft|published|archived>` - фильтр по статусу
- `search=<текст>` - поиск по названию/описанию/краткому описанию
- `ordering=<created_at|-created_at|title|-title|difficulty|-difficulty>` - сортировка
- `page=<номер>` - номер страницы
- `page_size=<число>` - количество элементов на странице

**Примеры URL:**

- `/courses/` - все курсы (только опубликованные для студентов)
- `/courses/?category=programming` - курсы категории с slug "programming"
- `/courses/?difficulty=beginner` - курсы для начинающих
- `/courses/?search=Python` - поиск по слову "Python"
- `/courses/?ordering=-created_at` - сортировка по дате (новые первые)
- `/courses/?page=2&page_size=10` - вторая страница по 10 курсов

**Пример ответа (200 OK):**

```json
{
  "count": 15,
  "next": "http://localhost:8000/api/courses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Основы Python",
      "slug": "osnovy-python",
      "short_description": "Базовый курс по программированию на Python",
      "teacher": 2,
      "teacher_name": "Мария Иванова",
      "category": 1,
      "category_name": "Программирование",
      "cover_image": null,
      "cover_image_url": null,
      "status": "published",
      "difficulty": "beginner",
      "duration_weeks": 8,
      "max_students": 30,
      "enrolled_count": 12,
      "is_featured": false,
      "created_at": "2025-11-24T10:30:00Z",
      "updated_at": "2025-11-24T11:00:00Z"
    }
  ]
}
```

---

### 2.3. Просмотр деталей курса

**Метод:** `GET`
**URL:** `/courses/<slug>/`
**Пример:** `/courses/osnovy-python/`

**Пример ответа (200 OK):**

```json
{
  "id": 1,
  "title": "Основы Python",
  "slug": "osnovy-python",
  "short_description": "Базовый курс по программированию на Python",
  "teacher": 2,
  "teacher_name": "Мария Иванова",
  "category": 1,
  "category_name": "Программирование",
  "cover_image": null,
  "cover_image_url": null,
  "status": "published",
  "difficulty": "beginner",
  "duration_weeks": 8,
  "max_students": 30,
  "enrolled_count": 12,
  "is_featured": false,
  "created_at": "2025-11-24T10:30:00Z",
  "updated_at": "2025-11-24T11:00:00Z",
  "description": "Полный курс по программированию на Python для начинающих. Изучите синтаксис, структуры данных, ООП и многое другое.",
  "lessons_count": 10,
  "assignments_count": 15,
  "is_enrolled": true,
  "progress": 35
}
```

**Примечание:**

- Поле `teacher` здесь содержит вложенный объект с подробной информацией о преподавателе в детальном представлении
- Поле `category` здесь содержит вложенный объект категории с полной информацией
- `is_enrolled` и `progress` доступны только для авторизованных пользователей

---

### 2.4. Записаться на курс (для студентов)

**Метод:** `POST`
**URL:** `/courses/<slug>/enroll/`
**Пример:** `/courses/osnovy-python/enroll/`
**Authorization:** Требуется (cookies, роль: student)

**Body:** Не требуется

**Пример ответа (201 Created):**

```json
{
  "detail": "Вы успешно записались на курс.",
  "enrollment": {
    "id": 5,
    "course_id": 1,
    "course_slug": "osnovy-python",
    "enrolled_at": "2025-11-24T15:30:00Z",
    "is_active": true,
    "progress": 0
  },
  "course": {
    "enrollments_count": 13,
    "spots_left": 17
  }
}
```

**Возможные ошибки:**

- `400 Bad Request` - "Достигнуто максимальное количество студентов."
- `400 Bad Request` - "Вы уже записаны на этот курс."

---

### 2.5. Отписаться от курса

**Метод:** `POST`
**URL:** `/courses/<slug>/unenroll/`
**Authorization:** Требуется (cookies, роль: student)

**Пример ответа (200 OK):**

```json
{
  "detail": "Вы отменили запись на курс.",
  "enrollment": {
    "id": 5,
    "course_id": 1,
    "course_slug": "osnovy-python",
    "is_active": false,
    "unenrolled_at": "2025-11-24T16:00:00Z"
  },
  "course": {
    "enrollments_count": 12,
    "spots_left": 18
  }
}
```

**Возможные ошибки:**

- `400 Bad Request` - "Вы не записаны на этот курс."

---

### 2.6. Получить опции фильтров

**Метод:** `GET`
**URL:** `/courses/filters/`

**Пример ответа (200 OK):**

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
        { "value": "-title", "label": "По названию (Я-А)" },
        {
          "value": "difficulty",
          "label": "По сложности (от простого к сложному)"
        },
        {
          "value": "-difficulty",
          "label": "По сложности (от сложного к простому)"
        }
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

**Примечание:** Категории динамически загружаются из базы данных. Значения категорий используют **slug**, а не ID.

---

## 3. Управление Занятиями (Уроками)

### 3.1. Создание урока (только для преподавателей)

**Метод:** `POST`
**URL:** `/lessons/`
**Headers:**

```
Content-Type: application/json
```

**Authorization:** Требуется (cookies, роль: teacher)

**Body (JSON):**

```json
{
  "course": "osnovy-python",
  "title": "Введение в Python",
  "slug": "vvedenie-v-python",
  "description": "Первый урок курса. Знакомство с языком Python.",
  "content": "# Введение в Python\n\nPython - это высокоуровневый язык программирования...",
  "order": 1,
  "duration_minutes": 45,
  "video_url": "https://youtube.com/watch?v=example",
  "is_published": true
}
```

**Примечание:**

- Поле `course` должно содержать **slug** курса (не ID)
- Поле `slug` опционально - создастся автоматически из `title`
- Поле `is_published` определяет, виден ли урок студентам (по умолчанию false)
- `order` - порядковый номер урока в курсе

**Пример ответа (201 Created):**

```json
{
  "id": 1,
  "course": "osnovy-python",
  "title": "Введение в Python",
  "slug": "vvedenie-v-python",
  "description": "Первый урок курса. Знакомство с языком Python.",
  "order": 1,
  "duration_minutes": 45,
  "is_published": true,
  "video_url": "https://youtube.com/watch?v=example",
  "materials_count": 0,
  "created_at": "2025-11-24T11:00:00Z",
  "updated_at": "2025-11-24T11:00:00Z"
}
```

---

### 3.2. Просмотр всех уроков курса

**Метод:** `GET`
**URL:** `/lessons/?course=<course_slug>`
**Пример:** `/lessons/?course=osnovy-python`

**Пример ответа (200 OK):**

```json
{
  "count": 12,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "course": "osnovy-python",
      "title": "Введение в Python",
      "slug": "vvedenie-v-python",
      "description": "Первый урок курса. Знакомство с языком Python.",
      "order": 1,
      "duration_minutes": 45,
      "is_published": true,
      "video_url": "https://youtube.com/watch?v=example1",
      "materials_count": 2,
      "created_at": "2025-11-24T11:00:00Z",
      "updated_at": "2025-11-24T11:00:00Z"
    },
    {
      "id": 2,
      "course": "osnovy-python",
      "title": "Переменные и типы данных",
      "slug": "peremennye-i-tipy-dannyh",
      "description": "Изучаем переменные, числа, строки и булевы значения.",
      "order": 2,
      "duration_minutes": 60,
      "is_published": true,
      "video_url": null,
      "materials_count": 3,
      "created_at": "2025-11-24T11:30:00Z",
      "updated_at": "2025-11-24T11:30:00Z"
    }
  ]
}
```

**Примечание:** Студенты видят только опубликованные уроки (`is_published: true`). Преподаватели видят все уроки.

---

### 3.3. Просмотр деталей урока

**Метод:** `GET`
**URL:** `/lessons/<lesson_slug>/`
**Пример:** `/lessons/vvedenie-v-python/`

**Пример ответа (200 OK):**

```json
{
  "id": 1,
  "course": {
    "id": 1,
    "title": "Основы Python",
    "slug": "osnovy-python",
    "short_description": "Базовый курс по программированию на Python",
    "teacher": 2,
    "teacher_name": "Мария Иванова",
    "category": 1,
    "category_name": "Программирование",
    "cover_image": null,
    "cover_image_url": null,
    "status": "published",
    "difficulty": "beginner",
    "duration_weeks": 8,
    "max_students": 30,
    "enrolled_count": 12,
    "is_featured": false,
    "created_at": "2025-11-24T10:30:00Z",
    "updated_at": "2025-11-24T11:00:00Z"
  },
  "title": "Введение в Python",
  "slug": "vvedenie-v-python",
  "description": "Первый урок курса. Знакомство с языком Python.",
  "order": 1,
  "duration_minutes": 45,
  "is_published": true,
  "video_url": "https://youtube.com/watch?v=example1",
  "materials_count": 2,
  "created_at": "2025-11-24T11:00:00Z",
  "updated_at": "2025-11-24T11:00:00Z",
  "content": "# Введение в Python\n\nPython - это высокоуровневый язык программирования...",
  "materials": [
    {
      "id": 1,
      "title": "Презентация урока",
      "file": "/media/lesson_materials/lesson1_slides.pdf",
      "file_url": "/media/lesson_materials/lesson1_slides.pdf",
      "file_type": "pdf",
      "file_size": 2048576,
      "description": "Слайды к первому уроку",
      "order": 1,
      "uploaded_at": "2025-11-24T11:05:00Z"
    }
  ],
  "assignments_count": 2
}
```

**Примечание:** В детальном представлении `course` содержит полный объект курса, а также добавляется поле `content` с текстом урока и список `materials`.

---

## 4. Управление Заданиями

### 4.1. Создание задания (только для преподавателей)

**Метод:** `POST`
**URL:** `/assignments/`
**Headers:**

```
Content-Type: application/json
```

**Authorization:** Требуется (cookies, роль: teacher)

**Body (JSON):**

```json
{
  "lesson": "vvedenie-v-python",
  "title": "Задание 1: Первая программа на Python",
  "description": "Напишите программу, которая выводит \"Hello, World!\"",
  "instructions": "1. Создайте файл hello.py\n2. Используйте функцию print()\n3. Загрузите файл в систему",
  "max_score": 100,
  "due_date": "2025-12-01T23:59:59Z",
  "is_required": true,
  "allow_late_submission": false
}
```

**Примечание:**

- Поле `lesson` должно содержать **slug** урока (не ID)
- `due_date` в формате ISO 8601 (опционально)
- `max_score` - максимальный балл за задание (по умолчанию 100)
- `is_required` - обязательное ли задание (по умолчанию false)
- `allow_late_submission` - разрешена ли поздняя сдача (по умолчанию false)logout

**Пример ответа (201 Created):**

```json
{
  "id": 1,
  "lesson": "vvedenie-v-python",
  "title": "Задание 1: Первая программа на Python",
  "description": "Напишите программу, которая выводит \"Hello, World!\"",
  "instructions": "1. Создайте файл hello.py\n2. Используйте функцию print()\n3. Загрузите файл в систему",
  "max_score": 100,
  "due_date": "2025-12-01T23:59:59Z",
  "is_required": true,
  "allow_late_submission": false,
  "files": [],
  "submissions_count": 0,
  "is_submitted": false,
  "created_at": "2025-11-24T12:00:00Z",
  "updated_at": "2025-11-24T12:00:00Z"
}
```

---

### 4.2. Просмотр всех заданий урока

**Метод:** `GET`
**URL:** `/assignments/?lesson=<lesson_slug>`
**Пример:** `/assignments/?lesson=vvedenie-v-python`

**Альтернативно, можно фильтровать по курсу:**
`/assignments/?course=<course_slug>`

**Пример ответа (200 OK):**

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "lesson": "vvedenie-v-python",
      "title": "Задание 1: Первая программа на Python",
      "description": "Напишите программу, которая выводит \"Hello, World!\"",
      "instructions": "1. Создайте файл hello.py\n2. Используйте функцию print()\n3. Загрузите файл в систему",
      "max_score": 100,
      "due_date": "2025-12-01T23:59:59Z",
      "is_required": true,
      "allow_late_submission": false,
      "files": [],
      "submissions_count": 8,
      "is_submitted": true,
      "created_at": "2025-11-24T12:00:00Z",
      "updated_at": "2025-11-24T12:00:00Z"
    }
  ]
}
```

**Примечание:** Поле `is_submitted` показывает, отправил ли текущий студент решение (доступно только для студентов).

---

### 4.3. Просмотр деталей задания

**Метод:** `GET`
**URL:** `/assignments/<assignment_id>/`
**Пример:** `/assignments/1/`

**Пример ответа (200 OK):**

```json
{
  "id": 1,
  "lesson": "vvedenie-v-python",
  "title": "Задание 1: Первая программа на Python",
  "description": "Напишите программу, которая выводит \"Hello, World!\"",
  "instructions": "1. Создайте файл hello.py\n2. Используйте функцию print()\n3. Загрузите файл в систему",
  "max_score": 100,
  "due_date": "2025-12-01T23:59:59Z",
  "is_required": true,
  "allow_late_submission": false,
  "files": [
    {
      "id": 1,
      "file": "/media/assignment_files/task1_template.py",
      "file_url": "/media/assignment_files/task1_template.py",
      "filename": "task1_template.py",
      "file_size": 1024,
      "uploaded_at": "2025-11-24T12:05:00Z"
    }
  ],
  "submissions_count": 8,
  "is_submitted": true,
  "created_at": "2025-11-24T12:00:00Z",
  "updated_at": "2025-11-24T12:00:00Z"
}
```

**Примечание:** Поле `files` содержит файлы, прикрепленные преподавателем к заданию (шаблоны, инструкции и т.д.).

---

## 5. Ответы студентов и Оценки

### 5.1. Отправка ответа на задание (студент)

**Метод:** `POST`
**URL:** `/submissions/`
**Headers:**

```
Content-Type: multipart/form-data
```

**Authorization:** Требуется (cookies, роль: student)

**Body (Form Data):**

```
assignment: 1
content: "Мой ответ на задание:\n\nprint('Hello, World!')"
```

**Для загрузки файлов используйте multipart/form-data с полем `file`**

**Примечание:**

- `assignment` - ID задания (не slug)
- `content` - текстовый ответ студента
- `file` - опциональный файл (можно загружать несколько файлов через модель SubmissionFile)
- Поле `student` устанавливается автоматически из текущего пользователя
- `is_late` определяется автоматически при создании

**Пример ответа (201 Created):**

```json
{
  "id": 15,
  "assignment": 1,
  "assignment_title": "Задание 1: Первая программа на Python",
  "student": 1,
  "student_name": "Иван Петров",
  "content": "Мой ответ на задание:\n\nprint('Hello, World!')",
  "status": "pending",
  "submitted_at": "2025-11-25T14:30:00Z",
  "updated_at": "2025-11-25T14:30:00Z",
  "is_late": false,
  "files_count": 0,
  "files": []
}
```

**Возможные статусы:**

- `pending` - ожидает проверки
- `graded` - проверено и оценено
- `returned` - возвращено на доработку

---

### 5.2. Просмотр своих ответов (студент)

**Метод:** `GET`
**URL:** `/submissions/`
**Authorization:** Требуется (cookies, роль: student)

**Query Parameters (опционально):**

- `assignment=<assignment_id>` - фильтр по конкретному заданию

**Пример ответа (200 OK):**

```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 15,
      "assignment": 1,
      "assignment_title": "Задание 1: Первая программа на Python",
      "student": 1,
      "student_name": "Иван Петров",
      "content": "Мой ответ на задание:\n\nprint('Hello, World!')",
      "status": "graded",
      "submitted_at": "2025-11-25T14:30:00Z",
      "updated_at": "2025-11-26T10:00:00Z",
      "is_late": false,
      "files_count": 1
    }
  ]
}
```

**Примечание:** Студенты видят только свои ответы автоматически.

---

### 5.3. Просмотр всех ответов студентов (преподаватель)

**Метод:** `GET`
**URL:** `/submissions/?assignment=<assignment_id>`
**Пример:** `/submissions/?assignment=1`
**Authorization:** Требуется (cookies, роль: teacher)

**Пример ответа (200 OK):**

```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 15,
      "assignment": 1,
      "assignment_title": "Задание 1: Первая программа на Python",
      "student": 1,
      "student_name": "Иван Петров",
      "content": "Мой ответ на задание:\n\nprint('Hello, World!')",
      "status": "pending",
      "submitted_at": "2025-11-25T14:30:00Z",
      "updated_at": "2025-11-25T14:30:00Z",
      "is_late": false,
      "files_count": 1
    },
    {
      "id": 16,
      "assignment": 1,
      "assignment_title": "Задание 1: Первая программа на Python",
      "student": 3,
      "student_name": "Анна Сидорова",
      "content": "print(\"Hello, World!\")",
      "status": "graded",
      "submitted_at": "2025-11-25T15:00:00Z",
      "updated_at": "2025-11-26T09:30:00Z",
      "is_late": false,
      "files_count": 0
    }
  ]
}
```

**Примечание:** Преподаватели видят все ответы на задания в своих курсах.

---

### 5.4. Выставление оценки (преподаватель)

**Метод:** `POST`
**URL:** `/grades/`
**Headers:**

```
Content-Type: application/json
```

**Authorization:** Требуется (cookies, роль: teacher)

**Body (JSON):**

```json
{
  "submission": 15,
  "score": 85,
  "feedback": "Отлично! Все пункты выполнены. Небольшое замечание: старайтесь следовать PEP 8 для оформления кода."
}
```

**Примечание:**

- `submission` - ID ответа студента
- `score` - балл (не может превышать `max_score` задания)
- `feedback` - комментарий преподавателя (опционально)
- Поле `graded_by` устанавливается автоматически
- После создания оценки статус ответа автоматически меняется на `graded`

**Пример ответа (201 Created):**

```json
{
  "id": 1,
  "submission": 15,
  "submission_content": "Мой ответ на задание:\n\nprint('Hello, World!')",
  "student_name": "Иван Петров",
  "assignment_title": "Задание 1: Первая программа на Python",
  "score": 85,
  "feedback": "Отлично! Все пункты выполнены. Небольшое замечание: старайтесь следовать PEP 8 для оформления кода.",
  "graded_by": 2,
  "graded_by_name": "Мария Иванова",
  "graded_at": "2025-11-26T10:00:00Z",
  "updated_at": "2025-11-26T10:00:00Z"
}
```

---

### 5.5. Просмотр оценок (студент)

**Метод:** `GET`
**URL:** `/grades/`
**Authorization:** Требуется (cookies, роль: student)

**Query Parameters (опционально):**

- `submission=<submission_id>` - фильтр по конкретному ответу

**Пример ответа (200 OK):**

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "submission": 15,
      "submission_content": "Мой ответ на задание:\n\nprint('Hello, World!')",
      "student_name": "Иван Петров",
      "assignment_title": "Задание 1: Первая программа на Python",
      "score": 85,
      "feedback": "Отлично! Все пункты выполнены. Небольшое замечание: старайтесь следовать PEP 8 для оформления кода.",
      "graded_by": 2,
      "graded_by_name": "Мария Иванова",
      "graded_at": "2025-11-26T10:00:00Z",
      "updated_at": "2025-11-26T10:00:00Z"
    }
  ]
}
```

**Примечание:** Студенты автоматически видят только свои оценки (где submission принадлежит им).

---

## 6. Категории курсов

### 6.1. Просмотр всех категорий

**Метод:** `GET`
**URL:** `/categories/`

**Пример ответа (200 OK):**

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Программирование",
      "slug": "programming",
      "description": "Курсы по различным языкам программирования и технологиям",
      "icon": "code",
      "created_at": "2025-11-20T10:00:00Z"
    },
    {
      "id": 2,
      "name": "Дизайн",
      "slug": "design",
      "description": "Курсы по графическому и веб-дизайну",
      "icon": "palette",
      "created_at": "2025-11-20T10:05:00Z"
    }
  ]
}
```

**Примечание:** Эндпоинт доступен всем пользователям (включая неавторизованных).

---

### 6.2. Создание категории (только admin/teacher)

**Метод:** `POST`
**URL:** `/categories/`
**Headers:**

```
Content-Type: application/json
```

**Authorization:** Требуется (cookies, роль: teacher или admin)

**Body (JSON):**

```json
{
  "name": "Программирование",
  "slug": "programming",
  "description": "Курсы по различным языкам программирования и технологиям",
  "icon": "code"
}
```

**Примечание:**

- Поле `slug` опционально - создастся автоматически из `name` если не указано
- Поле `icon` - название иконки (опционально)

**Пример ответа (201 Created):**

```json
{
  "id": 1,
  "name": "Программирование",
  "slug": "programming",
  "description": "Курсы по различным языкам программирования и технологиям",
  "icon": "code",
  "created_at": "2025-11-20T10:00:00Z"
}
```

---

## 7. Уведомления

### 7.1. Просмотр своих уведомлений

**Метод:** `GET`
**URL:** `/notifications/`
**Authorization:** Требуется (cookies)

**Query Parameters (опционально):**

- `is_read=<true|false>` - фильтр по статусу прочтения
- `type=<notification_type>` - фильтр по типу уведомления

**Примеры URL:**

- `/notifications/` - все уведомления
- `/notifications/?is_read=false` - только непрочитанные
- `/notifications/?type=assignment_deadline` - только уведомления о дедлайнах

**Пример ответа (200 OK):**

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "type": "assignment_deadline",
      "title": "Приближается дедлайн",
      "message": "До сдачи задания 'Переменные и типы данных' осталось 2 дня",
      "is_read": false,
      "read_at": null,
      "created_at": "2025-11-24T08:00:00Z"
    },
    {
      "id": 2,
      "type": "grade_received",
      "title": "Получена оценка",
      "message": "Преподаватель выставил оценку за задание: 85/100",
      "is_read": true,
      "read_at": "2025-11-23T15:00:00Z",
      "created_at": "2025-11-23T14:30:00Z"
    }
  ]
}
```

**Дополнительный эндпоинт для подсчета непрочитанных:**

**Метод:** `GET`
**URL:** `/notifications/unread_count/`

**Пример ответа (200 OK):**

```json
{
  "count": 2
}
```

---

### 7.2. Отметить уведомление как прочитанное

**Метод:** `POST`
**URL:** `/notifications/<notification_id>/mark_as_read/`
**Пример:** `/notifications/1/mark_as_read/`
**Authorization:** Требуется (cookies)

**Body:** Не требуется

**Пример ответа (200 OK):**

```json
{
  "id": 1,
  "type": "assignment_deadline",
  "title": "Приближается дедлайн",
  "message": "До сдачи задания 'Переменные и типы данных' осталось 2 дня",
  "is_read": true,
  "read_at": "2025-11-24T16:00:00Z",
  "created_at": "2025-11-24T08:00:00Z"
}
```

**Примечание:** После вызова метода поле `is_read` становится `true` и устанавливается `read_at`.

---

### 7.3. Отметить все уведомления как прочитанные

**Метод:** `POST`
**URL:** `/notifications/mark_all_as_read/`
**Authorization:** Требуется (cookies)

**Body:** Не требуется

**Пример ответа (200 OK):**

```json
{
  "detail": "Помечено 5 уведомлений как прочитанные."
}
```

**Примечание:** Возвращает количество обновленных уведомлений.

---

## 8. Дополнительные эндпоинты

### 8.1. Получение списка своих курсов (студент)

**Метод:** `GET`
**URL:** `/courses/my_courses/`
**Authorization:** Требуется (cookies, роль: student)

**Пример ответа (200 OK):**

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Основы Python",
      "slug": "osnovy-python",
      "short_description": "Базовый курс по программированию на Python",
      "teacher": 2,
      "teacher_name": "Мария Иванова",
      "category": 1,
      "category_name": "Программирование",
      "cover_image": null,
      "cover_image_url": null,
      "status": "published",
      "difficulty": "beginner",
      "duration_weeks": 8,
      "max_students": 30,
      "enrolled_count": 12,
      "is_featured": false,
      "created_at": "2025-11-24T10:30:00Z",
      "updated_at": "2025-11-24T11:00:00Z"
    }
  ]
}
```

**Примечание:**

- Для студентов возвращаются курсы, на которые они записаны (is_active=True)
- Для преподавателей возвращаются курсы, которые они ведут

---

### 8.2. Список студентов курса (преподаватель)

**Метод:** `GET`
**URL:** `/courses/<course_slug>/students/`
**Пример:** `/courses/osnovy-python/students/`
**Authorization:** Требуется (cookies, роль: teacher, владелец курса)

**Пример ответа (200 OK):**

```json
[
  {
    "id": 1,
    "username": "student_user",
    "email": "student@example.com",
    "first_name": "Иван",
    "last_name": "Петров",
    "enrolled_at": "2025-11-15T10:00:00Z",
    "progress": 35
  },
  {
    "id": 3,
    "username": "anna_s",
    "email": "anna@example.com",
    "first_name": "Анна",
    "last_name": "Сидорова",
    "enrolled_at": "2025-11-16T14:30:00Z",
    "progress": 50
  }
]
```

**Примечание:** Доступно только преподавателю, который ведет этот курс. Показывает только активных студентов (is_active=True).

---

## 9. Полезные советы для Insomnia/Postman

### 9.1. Настройка окружения (Environment)

Создайте переменные окружения для удобства:

```json
{
  "base_url": "http://localhost:8000/api",
  "course_slug": "osnovy-python",
  "lesson_id": "1",
  "assignment_id": "1"
}
```

Использование: `{{base_url}}/courses/{{course_slug}}/`

---

### 9.2. Автоматическая работа с cookies

В Insomnia/Postman cookies сохраняются автоматически после логина. Убедитесь, что включена опция:

- **Insomnia:** Preferences → Send cookies automatically
- **Postman:** Settings → Cookies → Automatically send cookies

---

### 9.3. Загрузка файлов (multipart/form-data)

При отправке файлов в задании:

1. Выберите тип Body: **Form Data** (не JSON)
2. Добавьте поля:
   - `answer_text` (Text)
   - `file` (File) - выберите файл с диска

---

### 9.4. Тестирование пагинации

Добавьте query параметры:

- `?page=2` - вторая страница
- `?page_size=10` - 10 элементов на странице

**Пример:** `{{base_url}}/courses/?page=2&page_size=10`
