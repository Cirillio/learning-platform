# JWT + Cookies: Детальная методичка для Nuxt 3 + Django Rest Framework

## 1. Теория: Что вообще происходит?

### 1.1 Проблема аутентификации в веб-приложениях

HTTP — это **stateless** протокол. Это значит, что каждый запрос от клиента к серверу — это отдельная изолированная операция. Сервер не помнит, кто ты такой между запросами.

**Пример проблемы:**

1. Ты вошёл на сайт (ввёл логин/пароль)
2. Сервер проверил данные — всё ОК
3. Ты переходишь на другую страницу
4. Сервер не знает, что ты — это ты, потому что HTTP не хранит состояние

**Решение:** Нужен способ, чтобы клиент при каждом запросе говорил серверу "Эй, это я, вот доказательство!"

### 1.2 Что такое JWT (JSON Web Token)?

JWT — это **компактный токен**, который содержит информацию о пользователе в зашифрованном виде.

**Структура JWT:** `header.payload.signature`

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImV4cCI6MTYxNjIzOTAyMn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Расшифровка частей:**

1. **Header** (заголовок):

   ```json
   {
     "alg": "HS256", // Алгоритм шифрования
     "typ": "JWT" // Тип токена
   }
   ```

2. **Payload** (данные):

   ```json
   {
     "user_id": 123,
     "email": "user@example.com",
     "exp": 1616239022 // Время истечения токена
   }
   ```

3. **Signature** (подпись):
   ```
   HMACSHA256(
     base64UrlEncode(header) + "." + base64UrlEncode(payload),
     secret_key
   )
   ```

**Ключевой момент:** Сервер создаёт JWT, используя секретный ключ. Клиент **не может изменить JWT** без этого ключа, потому что подпись перестанет совпадать.

### 1.3 Что такое Cookies?

Cookies — это **небольшие файлы данных**, которые браузер автоматически сохраняет и отправляет с каждым запросом на определённый домен.

**Пример:**

```http
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Strict
```

**Атрибуты cookies:**

- `HttpOnly` — JavaScript не может прочитать cookie (защита от XSS атак)
- `Secure` — Cookie отправляется только по HTTPS
- `SameSite=Strict` — Cookie отправляется только на тот же домен (защита от CSRF атак)
- `Max-Age=3600` — Срок жизни в секундах
- `Path=/` — На каких путях действует cookie

### 1.4 Зачем JWT + Cookies вместе?

**Проблема хранения JWT:**

1. **LocalStorage** — плохо, потому что:

   - Доступен из JavaScript → уязвим к XSS атакам
   - Если злоумышленник внедрит скрипт, он украдёт токен

2. **Cookies с HttpOnly** — хорошо, потому что:
   - JavaScript не может прочитать cookie
   - Браузер автоматически отправляет cookie с каждым запросом
   - Можно защитить от CSRF с помощью SameSite

**Итоговая схема:**

- JWT содержит данные о пользователе
- JWT хранится в cookie с флагом HttpOnly
- Браузер автоматически прикрепляет cookie к каждому запросу
- Сервер читает JWT из cookie и проверяет подпись

---

## 2. Бэкенд: Django Rest Framework

### 2.1 Установка зависимостей

```bash
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
```

**Зачем каждый пакет:**

- `djangorestframework` — API framework
- `djangorestframework-simplejwt` — готовая библиотека для работы с JWT
- `django-cors-headers` — для настройки CORS (Cross-Origin Resource Sharing)

### 2.2 Настройка Django (`settings.py`)

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'your_app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Должен быть в начале!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS настройки
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Адрес твоего Nuxt приложения
]
CORS_ALLOW_CREDENTIALS = True  # КРИТИЧНО! Позволяет отправлять cookies

# REST Framework настройки
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT настройки
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Короткий срок жизни
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    # Длинный срок жизни
    'ROTATE_REFRESH_TOKENS': True,  # Обновлять refresh token при использовании
    'BLACKLIST_AFTER_ROTATION': True,  # Блокировать старые refresh tokens
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_COOKIE': 'access_token',  # Название cookie для access token
    'AUTH_COOKIE_REFRESH': 'refresh_token',  # Название cookie для refresh token
    'AUTH_COOKIE_SECURE': True,  # Только HTTPS (в production)
    'AUTH_COOKIE_HTTP_ONLY': True,  # Защита от XSS
    'AUTH_COOKIE_SAMESITE': 'Lax',  # Защита от CSRF
}
```

**Объяснение настроек:**

- `CORS_ALLOW_CREDENTIALS = True` — БЕЗ ЭТОГО cookies не будут работать между доменами
- `ACCESS_TOKEN_LIFETIME` — короткий токен, который используется для запросов
- `REFRESH_TOKEN_LIFETIME` — длинный токен, который используется для обновления access token
- `ROTATE_REFRESH_TOKENS` — при обновлении выдаётся новый refresh token (безопаснее)
- `AUTH_COOKIE_HTTP_ONLY` — JavaScript не может прочитать cookie

### 2.3 Создание Views для аутентификации

```python
# your_app/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Логин пользователя.
    Принимает: { "email": "...", "password": "..." }
    Возвращает: Устанавливает cookies с токенами
    """
    email = request.data.get('email')
    password = request.data.get('password')

    # Аутентификация пользователя
    user = authenticate(username=email, password=password)

    if user is None:
        return Response(
            {'error': 'Неверный email или пароль'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Создаём JWT токены
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Создаём ответ
    response = Response({
        'message': 'Успешный вход',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        }
    }, status=status.HTTP_200_OK)

    # Устанавливаем cookies с токенами
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,  # Защита от XSS
        secure=True,    # Только HTTPS (в production убери на False для localhost)
        samesite='Lax', # Защита от CSRF
        max_age=900,    # 15 минут (в секундах)
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='Lax',
        max_age=604800,  # 7 дней (в секундах)
    )

    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    """
    Выход пользователя.
    Удаляет cookies с токенами.
    """
    response = Response({
        'message': 'Успешный выход'
    }, status=status.HTTP_200_OK)

    # Удаляем cookies
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Обновление access token с помощью refresh token.
    Читает refresh_token из cookie.
    """
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response(
            {'error': 'Refresh token не найден'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        # Создаём новый access token
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        response = Response({
            'message': 'Token обновлён'
        }, status=status.HTTP_200_OK)

        # Обновляем cookie с access token
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=900,
        )

        return response

    except Exception as e:
        return Response(
            {'error': 'Невалидный refresh token'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Получение данных текущего пользователя.
    Требует валидный access token в cookie.
    """
    user = request.user
    return Response({
        'id': user.id,
        'email': user.email,
        'username': user.username,
    })
```

**Что происходит в коде:**

1. **login()** — проверяет логин/пароль, создаёт JWT токены, кладёт их в cookies
2. **logout()** — удаляет cookies с токенами
3. **refresh_token()** — читает refresh token из cookie, создаёт новый access token
4. **get_current_user()** — защищённый эндпоинт, требует аутентификации

### 2.4 Middleware для чтения JWT из cookies

По умолчанию DRF ищет JWT в заголовке `Authorization: Bearer <token>`. Нам нужно научить его читать из cookies.

```python
# your_app/middleware.py

class JWTAuthFromCookieMiddleware:
    """
    Middleware для чтения JWT из cookie и добавления в заголовок Authorization.
    DRF ожидает токен в заголовке, но мы храним его в cookie.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Читаем access token из cookie
        access_token = request.COOKIES.get('access_token')

        # Если токен есть, добавляем его в заголовок
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        response = self.get_response(request)
        return response
```

**Добавь middleware в `settings.py`:**

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'your_app.middleware.JWTAuthFromCookieMiddleware',  # Добавь сюда!
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### 2.5 URLs (`urls.py`)

```python
# your_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/refresh/', views.refresh_token, name='refresh_token'),
    path('auth/me/', views.get_current_user, name='current_user'),
]
```

```python
# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('your_app.urls')),
]
```

---

## 3. Фронтенд: Nuxt 3 (TypeScript)

### 3.1 Установка зависимостей

```bash
pnpm add @pinia/nuxt pinia
```

**Зачем Pinia?** — Для хранения состояния пользователя (например, данных о юзере)

### 3.2 Настройка Nuxt (`nuxt.config.ts`)

```typescript
// nuxt.config.ts

export default defineNuxtConfig({
  modules: ["@pinia/nuxt"],

  runtimeConfig: {
    public: {
      apiBase: "http://localhost:8000/api", // Адрес Django API
    },
  },
});
```

### 3.3 Composable для API запросов

Создадим удобный composable для работы с API.

```typescript
// composables/useApi.ts

export const useApi = () => {
  const config = useRuntimeConfig();
  const baseURL = config.public.apiBase;

  /**
   * Wrapper для $fetch с автоматической обработкой credentials.
   * credentials: 'include' критично для отправки cookies!
   */
  const apiFetch = $fetch.create({
    baseURL,
    credentials: "include", // КРИТИЧНО! Отправляет cookies с запросом
  });

  return {
    apiFetch,
  };
};
```

**Объяснение:**

- `credentials: 'include'` — БЕЗ ЭТОГО браузер не будет отправлять cookies на другой домен
- `baseURL` — базовый URL для всех запросов

### 3.4 Composable для аутентификации

```typescript
// composables/useAuth.ts

interface User {
  id: number;
  email: string;
  username: string;
}

interface LoginCredentials {
  email: string;
  password: string;
}

export const useAuth = () => {
  const { apiFetch } = useApi();
  const user = useState<User | null>("user", () => null);
  const isAuthenticated = computed(() => !!user.value);

  /**
   * Вход в систему
   */
  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await apiFetch("/auth/login/", {
        method: "POST",
        body: credentials,
      });

      // После успешного логина получаем данные пользователя
      await fetchUser();

      return { success: true, data: response };
    } catch (error: any) {
      return {
        success: false,
        error: error.data?.error || "Ошибка входа",
      };
    }
  };

  /**
   * Выход из системы
   */
  const logout = async () => {
    try {
      await apiFetch("/auth/logout/", {
        method: "POST",
      });

      user.value = null;

      // Перенаправляем на страницу логина
      await navigateTo("/login");

      return { success: true };
    } catch (error) {
      return { success: false };
    }
  };

  /**
   * Получение данных текущего пользователя
   */
  const fetchUser = async () => {
    try {
      const data = await apiFetch<User>("/auth/me/");
      user.value = data;
      return { success: true, data };
    } catch (error) {
      user.value = null;
      return { success: false };
    }
  };

  /**
   * Обновление access token
   */
  const refreshToken = async () => {
    try {
      await apiFetch("/auth/refresh/", {
        method: "POST",
      });
      return { success: true };
    } catch (error) {
      user.value = null;
      return { success: false };
    }
  };

  return {
    user,
    isAuthenticated,
    login,
    logout,
    fetchUser,
    refreshToken,
  };
};
```

### 3.5 Middleware для защиты страниц

```typescript
// middleware/auth.ts

export default defineNuxtRouteMiddleware(async (to, from) => {
  const { isAuthenticated, fetchUser } = useAuth();

  // Если пользователь не загружен, пытаемся загрузить
  if (!isAuthenticated.value) {
    const result = await fetchUser();

    // Если не удалось загрузить пользователя, редирект на логин
    if (!result.success) {
      return navigateTo("/login");
    }
  }
});
```

### 3.6 Plugin для автоматического обновления токена

```typescript
// plugins/auth.client.ts

export default defineNuxtPlugin(() => {
  const { refreshToken, fetchUser } = useAuth();

  // Обновляем токен каждые 14 минут (access token живёт 15 минут)
  setInterval(async () => {
    const result = await refreshToken();

    if (result.success) {
      console.log("Access token обновлён");
    } else {
      console.log("Не удалось обновить токен");
    }
  }, 14 * 60 * 1000); // 14 минут в миллисекундах

  // При загрузке приложения пытаемся загрузить пользователя
  fetchUser();
});
```

**Объяснение:**

- Каждые 14 минут автоматически обновляем access token
- При загрузке приложения проверяем, авторизован ли пользователь

### 3.7 Страница логина

```vue
<!-- pages/login.vue -->

<script setup lang="ts">
definePageMeta({
  middleware: ["auth"],
  // Если пользователь уже авторизован, редирект на главную
  // Но это обработает middleware
});

const { login } = useAuth();
const router = useRouter();

const form = reactive({
  email: "",
  password: "",
});

const error = ref<string | null>(null);
const loading = ref(false);

const handleLogin = async () => {
  error.value = null;
  loading.value = true;

  const result = await login(form);

  loading.value = false;

  if (result.success) {
    // Успешный вход, перенаправляем на главную
    await router.push("/");
  } else {
    error.value = result.error || "Ошибка входа";
  }
};
</script>

<template>
  <div class="container">
    <h1>Вход в систему</h1>

    <form @submit.prevent="handleLogin">
      <div>
        <label for="email">Email:</label>
        <input id="email" v-model="form.email" type="email" required />
      </div>

      <div>
        <label for="password">Пароль:</label>
        <input id="password" v-model="form.password" type="password" required />
      </div>

      <div v-if="error" class="error">
        {{ error }}
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? "Загрузка..." : "Войти" }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
}

.error {
  color: red;
  margin: 10px 0;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
```

### 3.8 Защищённая страница

```vue
<!-- pages/index.vue -->

<script setup lang="ts">
definePageMeta({
  middleware: ["auth"], // Только для авторизованных пользователей
});

const { user, logout } = useAuth();

const handleLogout = async () => {
  await logout();
};
</script>

<template>
  <div class="container">
    <h1>Добро пожаловать, {{ user?.username }}!</h1>

    <p>Email: {{ user?.email }}</p>

    <button @click="handleLogout">Выйти</button>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
}
</style>
```

---

## 4. Безопасность и Best Practices

### 4.1 HTTPS обязателен в production

**Почему:**

- Без HTTPS cookies с флагом `Secure` не будут работать
- Без HTTPS токены могут быть перехвачены

**Как настроить:**

- В production используй Let's Encrypt для бесплатного SSL
- На localhost можешь убрать `secure=True` в Django и тестировать

### 4.2 Защита от XSS (Cross-Site Scripting)

**Что это:** Злоумышленник внедряет JavaScript код на твою страницу.

**Как защититься:**

- ✅ `HttpOnly` cookies — JavaScript не может прочитать токены
- ✅ Экранируй пользовательский ввод в Vue (Vue делает это автоматически)
- ✅ Используй Content Security Policy (CSP)

### 4.3 Защита от CSRF (Cross-Site Request Forgery)

**Что это:** Злоумышленник отправляет запрос от имени пользователя с другого сайта.

**Как защититься:**

- ✅ `SameSite=Lax` или `SameSite=Strict` в cookies
- ✅ CORS настройка — только разрешённые домены
- ✅ Проверка origin/referer на сервере

### 4.4 Короткий срок жизни access token

**Почему:**

- Access token используется часто → больше шансов утечки
- Короткий срок (15 минут) минимизирует ущерб от утечки

**Как:**

- Access token: 15 минут
- Refresh token: 7 дней
- Автоматическое обновление access token через plugin

### 4.5 Хранение секретного ключа Django

**НИКОГДА не коммить SECRET_KEY в Git!**

```python
# settings.py

import os
from pathlib import Path

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-key-for-localhost-only')
```

**Используй `.env` файл:**

```bash
# .env
DJANGO_SECRET_KEY=your-super-secret-key-here
```

### 4.6 Rotate refresh tokens

```python
# settings.py

SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,  # При обновлении выдавать новый refresh token
    'BLACKLIST_AFTER_ROTATION': True,  # Блокировать старые refresh tokens
}
```

**Зачем:**

- Если refresh token украли, злоумышленник не сможет использовать его бесконечно
- После первого использования токен становится невалидным

---

## 5. Docker setup (опционально)

### 5.1 Dockerfile для Django

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 5.2 Dockerfile для Nuxt

```dockerfile
# frontend/Dockerfile

FROM node:20-alpine

WORKDIR /app

RUN npm install -g pnpm

COPY package.json pnpm-lock.yaml ./
RUN pnpm install

COPY . .

CMD ["pnpm", "dev", "--host"]
```

### 5.3 docker-compose.yml

```yaml
version: "3.8"

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/myapp
      DJANGO_SECRET_KEY: your-secret-key
    depends_on:
      - db

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      API_BASE_URL: http://backend:8000/api

volumes:
  postgres_data:
```

---

## 6. Типичные ошибки и их решения

### Ошибка: Cookies не отправляются на сервер

**Причина:** Не указан `credentials: 'include'` в fetch.

**Решение:**

```typescript
const apiFetch = $fetch.create({
  credentials: "include", // Добавь это!
});
```

---

### Ошибка: CORS error в браузере

**Причина:** Не настроен CORS на Django или не разрешены credentials.

**Решение:**

```python
# settings.py

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True  # Обязательно!
```

---

### Ошибка: JWT token не читается на сервере

**Причина:** Middleware не добавлен или добавлен в неправильном месте.

**Решение:** Убедись, что `JWTAuthFromCookieMiddleware` добавлен в `MIDDLEWARE` после `AuthenticationMiddleware`.

---

### Ошибка: "Refresh token не найден"

**Причина:** Cookie не сохранился или истёк срок действия.

**Решение:**

- Проверь, что `httponly`, `secure`, `samesite` правильно настроены
- Проверь, что `max_age` не слишком короткий
- В DevTools → Application → Cookies проверь наличие cookie

---

### Ошибка: Token expired

**Причина:** Access token истёк (живёт 15 минут).

**Решение:** Автоматическое обновление через plugin:

```typescript
// plugins/auth.client.ts

setInterval(async () => {
  await refreshToken();
}, 14 * 60 * 1000);
```

---

## 7. Проверка работы системы

### Шаг 1: Запусти Django

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Шаг 2: Запусти Nuxt

```bash
cd frontend
pnpm install
pnpm dev
```

### Шаг 3: Тестируй в браузере

1. Открой `http://localhost:3000/login`
2. Введи логин/пароль
3. После успешного входа открой DevTools → Application → Cookies
4. Должны появиться cookies: `access_token` и `refresh_token` с флагами `HttpOnly`, `Secure`, `SameSite`
5. Перейди на главную страницу — должно показать твоё имя
6. Обнови страницу — должен остаться залогиненным
7. Жди 15 минут → access token автоматически обновится

---

## 8. Итоговая схема работы

```
1. Пользователь вводит логин/пароль
   ↓
2. Nuxt отправляет POST /api/auth/login/ { email, password }
   ↓
3. Django проверяет credentials
   ↓
4. Django создаёт JWT (access + refresh)
   ↓
5. Django устанавливает cookies: access_token, refresh_token
   ↓
6. Браузер сохраняет cookies
   ↓
7. При следующем запросе браузер автоматически отправляет cookies
   ↓
8. Django middleware читает access_token из cookie
   ↓
9. Django проверяет подпись JWT
   ↓
10. Если подпись валидна → идентифицирует пользователя
    ↓
11. Через 14 минут Nuxt автоматически обновляет access_token
    ↓
12. Django создаёт новый access_token используя refresh_token
    ↓
13. Цикл повторяется
```

---

## 9. Чеклист финальной проверки

- [ ] Django установлен и настроен
- [ ] djangorestframework-simplejwt установлен
- [ ] CORS настроен с `CORS_ALLOW_CREDENTIALS = True`
- [ ] JWT настроен с правильными lifetime
- [ ] Middleware `JWTAuthFromCookieMiddleware` добавлен
- [ ] Views для login, logout, refresh созданы
- [ ] Nuxt установлен с Pinia
- [ ] `credentials: 'include'` в fetch
- [ ] Composable `useAuth` создан
- [ ] Middleware для защиты страниц создан
- [ ] Plugin для автообновления токена создан
- [ ] В production используется HTTPS
- [ ] SECRET_KEY не закоммичен в Git
- [ ] Cookies имеют флаги `HttpOnly`, `Secure`, `SameSite`

---

**Всё! Теперь у тебя полноценная аутентификация JWT + Cookies с автоматическим обновлением токенов, защитой от XSS/CSRF и правильным хранением в HttpOnly cookies.**
