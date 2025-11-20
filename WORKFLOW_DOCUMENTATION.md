# Документация по API для учебного портала

Этот документ описывает, как использовать API бэкенда для выполнения всех основных операций, предусмотренных в задании.

**Базовый URL для всех запросов:** `http://localhost:8000`

## 1. Аутентификация и Управление профилем

API использует JWT-токены, которые автоматически устанавливаются в `HttpOnly` cookies (`access_token` и `refresh_token`) после успешной регистрации или входа. Вам не нужно вручную добавлять их в заголовки.

### 1.1. Регистрация (создание студента)

Создает нового пользователя с ролью "студент".

- **Endpoint:** `POST /api/auth/register/`
- **Permissions:** Любой (неаутентифицированный) пользователь.
- **Request Body:**
  ```json
  {
    "email": "student@example.com",
    "password": "yourstrongpassword",
    "first_name": "Имя",
    "last_name": "Фамилия"
  }
  ```

### 1.2. Вход в систему

Аутентифицирует пользователя и устанавливает cookies.

- **Endpoint:** `POST /api/auth/login/`
- **Permissions:** Любой (неаутентифицированный) пользователь.
- **Request Body:**
  ```json
  {
    "email": "student@example.com",
    "password": "yourstrongpassword"
  }
  ```

### 1.3. Выход из системы

Удаляет аутентификационные cookies.

- **Endpoint:** `POST /api/auth/logout/`
- **Permissions:** Аутентифицированный пользователь.

### 1.4. Управление профилем

Просмотр и обновление данных своего профиля.

- **Endpoint:** `GET`, `PUT`, `PATCH` `/api/auth/profile/`
- **Permissions:** Аутентифицированный пользователь.
- **Request Body (для `PUT`/`PATCH`):**
  ```json
  {
    "first_name": "НовоеИмя",
    "last_name": "НоваяФамилия",
    "bio": "Краткая биография..."
  }
  ```

---

## 2. Рабочий процесс Преподавателя

Для выполнения этих действий пользователь должен иметь роль "преподаватель" (`is_teacher=True`). Создание преподавателей производится через админ-панель Django.

### 2.1. Управление курсами

- **Создать курс:**
  - **Endpoint:** `POST /api/courses/`
  - **Request Body:**
    ```json
    {
      "title": "Введение в Python",
      "description": "Основы программирования на Python.",
      "is_published": true
    }
    ```

- **Просмотреть свои курсы:**
  - **Endpoint:** `GET /api/courses/` (автоматически фильтруется для текущего преподавателя)

- **Обновить/Удалить курс:**
  - **Endpoint:** `PUT/PATCH/DELETE /api/courses/{slug}/`

### 2.2. Управление уроками

- **Создать урок для курса:**
  - **Endpoint:** `POST /api/lessons/`
  - **Request Body:**
    ```json
    {
      "course": 1, // ID курса, к которому относится урок
      "title": "Урок 1: Переменные и типы данных",
      "content": "Текст урока..."
    }
    ```

- **Просмотреть уроки курса:**
  - **Endpoint:** `GET /api/lessons/?course_slug={slug}`

- **Обновить/Удалить урок:**
  - **Endpoint:** `PUT/PATCH/DELETE /api/lessons/{id}/`

### 2.3. Управление заданиями

- **Создать задание для урока:**
  - **Endpoint:** `POST /api/assignments/`
  - **Request Body:**
    ```json
    {
      "lesson": 1, // ID урока
      "title": "Домашнее задание 1",
      "description": "Напишите функцию, которая...",
      "due_date": "2025-12-31T23:59:59Z"
    }
    ```

- **Просмотреть задания урока:**
  - **Endpoint:** `GET /api/assignments/?lesson_id={id}`

- **Обновить/Удалить задание:**
  - **Endpoint:** `PUT/PATCH/DELETE /api/assignments/{id}/`

### 2.4. Проверка ответов и выставление оценок

- **Просмотреть все ответы на задания:**
  - **Endpoint:** `GET /api/submissions/`
  - **Query Params (для фильтрации):** `?assignment_id={id}`

- **Выставить/обновить оценку:**
  - **Создание оценки:** `POST /api/grades/`
  - **Обновление оценки:** `PUT/PATCH /api/grades/{id}/`
  - **Request Body:**
    ```json
    {
      "submission": 1, // ID ответа студента
      "score": 5,
      "feedback": "Отличная работа!"
    }
    ```

---

## 3. Рабочий процесс Студента

Для выполнения этих действий пользователь должен иметь роль "студент".

### 3.1. Взаимодействие с курсами

- **Просмотреть все опубликованные курсы:**
  - **Endpoint:** `GET /api/courses/`

- **Записаться на курс:**
  - **Endpoint:** `POST /api/courses/{slug}/enroll/`
  - **Permissions:** Аутентифицированный студент.

### 3.2. Просмотр учебных материалов

- **Просмотреть уроки курса (на который записан):**
  - **Endpoint:** `GET /api/lessons/?course_slug={slug}`

- **Просмотреть задания урока:**
  - **Endpoint:** `GET /api/assignments/?lesson_id={id}`

### 3.3. Отправка ответов на задания

- **Отправить ответ на задание:**
  - **Endpoint:** `POST /api/submissions/`
  - **Request Body:**
    ```json
    {
      "assignment": 1, // ID задания
      "content": "Вот мой ответ...",
      "file_attachment": null // или файл
    }
    ```

- **Просмотреть/изменить свои ответы:**
  - **Endpoint:** `GET /api/submissions/` (автоматически фильтруется для текущего студента)
  - **Endpoint для обновления:** `PUT/PATCH /api/submissions/{id}/`

### 3.4. Просмотр оценок

- **Просмотреть свои оценки:**
  - **Endpoint:** `GET /api/grades/` (автоматически фильтруется для текущего студента)
  - **Пример ответа:**
    ```json
    [
      {
        "id": 1,
        "submission": 1,
        "score": 5,
        "feedback": "Отличная работа!",
        "teacher": 2,
        "date_graded": "2025-11-21T10:00:00Z"
      }
    ]
    ```
