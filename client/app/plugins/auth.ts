// plugins/auth.ts

import type { User, UserProfile } from "~/types";
import { normalizeUser } from "~/utils/get-user-from-profile";

export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore();

  // Используем useState для передачи данных между SSR и клиентом
  // Храним уже нормализованного пользователя
  const ssrUser = useState<User | null>("ssr-user", () => null);

  // На сервере читаем из context и сохраняем в useState
  if (import.meta.server) {
    const event = useRequestEvent();
    console.log("🔍 [SSR] Event context user:", event?.context.user?.username);
    if (event?.context.user) {
      // event.context.user - это RawUserProfile (с бэкенда)
      // Нормализуем его в User (Internal)
      const normalizedUser = normalizeUser(event.context.user as UserProfile);

      ssrUser.value = normalizedUser;
      authStore.setUser(normalizedUser);
      console.log("✅ [SSR] User set from context:", normalizedUser.username);
    }
  }

  // На клиенте используем данные из useState (гидратация из SSR)
  if (import.meta.client) {
    console.log("🔍 [Client] SSR user:", ssrUser.value);

    if (ssrUser.value) {
      // Есть данные из SSR - используем их
      authStore.setUser(ssrUser.value);
      console.log(
        "✅ [Client] User hydrated from SSR:",
        ssrUser.value.username
      );
    } else {
      // SSR не вернул пользователя.
      // Поскольку access_token обычно HttpOnly, мы не можем надежно проверить его наличие через document.cookie.
      // Мы полагаемся на то, что Server Middleware уже попытался авторизовать пользователя.
      // Если ssrUser пуст, значит сервер считает нас гостем.

      if (authStore.isAuthenticated) {
        authStore.clearAuth();
      }
    }
  }
});
