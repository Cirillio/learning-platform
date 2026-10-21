# Авторизация

JWT (access + refresh) живут только в HttpOnly-cookies. JavaScript к токенам доступа
не имеет; на клиенте хранится лишь объект пользователя.

## Участники

| Где | Файл | Роль |
| :--- | :--- | :--- |
| Django | `users/views.py` (`LoginView`, `RefreshTokenView`, `LogoutView`) | Ставит и удаляет cookies `access_token`, `refresh_token`, `auth_remember_me`. |
| Django | `users/middleware.py` | Копирует `access_token` из cookie в заголовок `Authorization: Bearer …` для DRF. |
| Nitro | `client/server/middleware/auth.ts` | На каждый SSR-запрос загружает профиль; если access истёк — обновляет его через refresh и пробрасывает новые `set-cookie` в браузер. Результат кладёт в `event.context.user`. |
| Nuxt plugin | `app/plugins/auth.ts` | На сервере берёт пользователя из `event.context.user`, нормализует и кладёт в store и `useState("ssr-user")`. На клиенте гидрирует store из `useState`. |
| Store | `app/stores/auth.ts` | `user`, `isLoading`, `error`; геттеры `isAuthenticated`, `isTeacher`, `isStudent`, `userRole`. |
| API-клиент | `app/composables/useApi.ts` | `credentials: "include"`; на SSR пробрасывает заголовок `Cookie`; при 401 делает один refresh (mutex) и повторяет запрос. |
| Composable | `app/composables/useAuth.ts` | `login`, `register` (с автологином), `logout`. |
| Route middleware | `app/middleware/*.ts` | Доступ по ролям — см. `architecture.md`. |

## Время жизни

- Access — 15 минут.
- Refresh — 7 дней (`SIMPLE_JWT`), ротация с blacklist старого токена.
- `remember_me: true` — refresh-cookie живёт 30 дней; `false` — сессионная cookie.
- Cookies: `HttpOnly`, `Secure`, `SameSite=Lax`.

## Потоки

**Логин.** `useAuth().login()` → `POST /auth/login/` → бэкенд ставит cookies и возвращает
`user` → store → переход на `/profile`.

**Первая загрузка (SSR).** Nitro-middleware проверяет cookies → профиль (при необходимости
после refresh) → `plugins/auth.ts` кладёт пользователя в store → состояние уходит на клиент
через `useState`. Защищённые страницы рендерятся без «мигания» гостевого состояния.

**Навигация на клиенте.** Store уже заполнен; route middleware проверяют роль.
Если какой-то запрос получил 401, `useApi` обновляет токен и повторяет запрос; если refresh
не удался — store очищается и происходит переход на `/auth/login`.

**Выход.** `POST /auth/logout/` удаляет cookies, store очищается.

## Требования к окружению

- CORS: `CORS_ALLOWED_ORIGINS` содержит адрес фронта, `CORS_ALLOW_CREDENTIALS = True`.
- Redis запущен: логин ставит Celery-задачу (письмо о входе), без брокера запрос зависает.

## Диагностика

- **После логина снова гость.** Проверить, что cookies ставятся (DevTools → Application →
  Cookies) и фронт открыт с origin из `CORS_ALLOWED_ORIGINS`.
- **На SSR 401 при `/auth/profile/`.** Cookie не дошла до бэкенда — смотреть логи
  Nitro-middleware (`[Server Middleware]`).
- **HMR выкидывает на логин.** В dev это ожидаемо: состояние сбрасывается и
  восстанавливается по cookies при следующей загрузке.
