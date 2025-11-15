// plugins/auth.ts

import type { User } from "~/types";

export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore();

  // Используем useState для передачи данных между SSR и клиентом
  const ssrUser = useState<User | null>("ssr-user", () => null);

  // На сервере читаем из context и сохраняем в useState
  if (process.server) {
    const event = useRequestEvent();
    console.log("🔍 [SSR] Event context user:", event?.context.user);
    if (event?.context.user) {
      ssrUser.value = event.context.user;
      authStore.setUser(event.context.user);
      console.log(
        "✅ [SSR] User set from context:",
        event.context.user.username
      );
    }
  }

  // На клиенте используем данные из useState (гидратация из SSR)
  if (process.client) {
    console.log("🔍 [Client] SSR user:", ssrUser.value);

    if (ssrUser.value) {
      // Есть данные из SSR - используем их
      authStore.setUser(ssrUser.value);
      console.log(
        "✅ [Client] User hydrated from SSR:",
        ssrUser.value.username
      );
    } else {
      // Нет данных из SSR - проверяем cookies
      const cookies = document.cookie;
      const hasToken = cookies.includes("access_token=");

      console.log(
        "🔍 [Client] Has token:",
        hasToken,
        "Is authenticated:",
        authStore.isAuthenticated
      );

      if (hasToken && !authStore.isAuthenticated) {
        // Есть токен, но юзера нет - грузим
        console.log("🔄 [Client] Loading user profile...");
        try {
          const api = useApi();
          const user = await api.getProfile();
          authStore.setUser(user);
          console.log("✅ [Client] User loaded:", user.username);
        } catch (e) {
          // Токен невалидный
          console.error("❌ [Client] Failed to load user:", e);
          authStore.clearAuth();
        }
      }
    }
  }
});
