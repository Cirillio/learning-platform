// server/middleware/auth.ts
export default defineEventHandler(async (event) => {
  const path = event.path;
  if (path.startsWith("/api") || path.startsWith("/_nuxt")) {
    return;
  }

  const config = useRuntimeConfig();
  const cookies = parseCookies(event);
  let accessToken = cookies.access_token;

  // 1. Первая попытка: получить пользователя с текущим access_token
  if (accessToken) {
    try {
      const user = await $fetch("/auth/profile/", {
        baseURL: config.public.apiBase,
        headers: { 'Cookie': `access_token=${accessToken}` }
      });
      event.context.user = user;
      console.log("✅ [Server Middleware] Пользователь загружен с существующим токеном.");
      return; // Успех, выходим
    } catch (error: any) {
      console.log("⚠️ [Server Middleware] Не удалось получить пользователя, токен мог истечь.");
    }
  }

  // 2. Вторая попытка: если токена не было или он истек, используем refresh_token
  const refreshToken = cookies.refresh_token;
  if (!refreshToken) {
    event.context.user = null;
    return; // Нет refresh_token, сессию не восстановить
  }

  console.log("🔄 [Server Middleware] Попытка обновить токен на сервере...");
  try {
    // Вызываем эндпоинт обновления. Используем .raw() для доступа к заголовкам ответа.
    const refreshResponse = await $fetch.raw("/auth/refresh/", {
      method: 'POST',
      baseURL: config.public.apiBase,
      headers: { 'Cookie': `refresh_token=${refreshToken}` }
    });

    // Бэкенд в ответ на /refresh/ должен установить новые cookie.
    // Мы должны "пробросить" эти заголовки 'set-cookie' в браузер пользователя.
    const setCookieHeaders = refreshResponse.headers.getSetCookie();
    if (setCookieHeaders.length > 0) {
      setCookieHeaders.forEach(cookie => {
        appendHeader(event, 'set-cookie', cookie);
      });

      // Теперь нам нужен новый access_token, чтобы получить пользователя в этом же запросе.
      // Мы парсим его из заголовков, которые собираемся отправить в браузер.
      for (const cookie of setCookieHeaders) {
        if (cookie.startsWith('access_token=')) {
          accessToken = cookie.split(';')[0].split('=')[1];
          break;
        }
      }
    }

    if (!accessToken) {
      throw new Error("Ответ от /refresh/ не содержит новый access_token.");
    }

    // 3. Третья попытка: получить пользователя с новым access_token
    console.log("✅ [Server Middleware] Токен обновлен. Повторная попытка получить пользователя...");
    const user = await $fetch("/auth/profile/", {
      baseURL: config.public.apiBase,
      headers: { 'Cookie': `access_token=${accessToken}` }
    });
    event.context.user = user;
    console.log("✅ [Server Middleware] Пользователь успешно загружен после обновления.");

  } catch (error) {
    console.error("❌ [Server Middleware] Refresh token невалиден или произошла ошибка. Сессия очищена.", error);
    event.context.user = null;
    // Очищаем невалидные cookie в браузере пользователя
    deleteCookie(event, 'access_token');
    deleteCookie(event, 'refresh_token');
    deleteCookie(event, 'auth_remember_me');
  }
});

