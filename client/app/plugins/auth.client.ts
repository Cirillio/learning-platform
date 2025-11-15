// plugins/auth.client.ts
export default defineNuxtPlugin(async () => {
  console.log("🌐 [Client Plugin] auth.client.ts STARTED");

  const authStore = useAuthStore();
  console.log(
    "🔍 [Client Plugin] authStore.isAuthenticated:",
    authStore.isAuthenticated
  );
  console.log(
    "🔍 [Client Plugin] authStore.user:",
    authStore.user?.username || "null"
  );
  const { getProfile, refreshToken } = useApi();
  const router = useRouter();

  let intervalId: number | undefined;
  let refreshingPromise: Promise<void> | null = null;
  let lastRefreshTime = 0;
  const MIN_REFRESH_INTERVAL = 60 * 1000;

  const bc =
    typeof BroadcastChannel !== "undefined"
      ? new BroadcastChannel("auth")
      : null;
  if (bc) {
    bc.onmessage = (e) => {
      if (e.data?.type === "logout") {
        authStore.clearAuth();
        if (!router.currentRoute.value.path.startsWith("/auth/")) {
          router.push("/auth/login");
        }
      }
      if (e.data?.type === "refresh-done") {
        refreshingPromise = null;
        lastRefreshTime = Date.now();
      }
    };
  }

  async function safeRefresh() {
    if (!authStore.isAuthenticated) return;
    if (refreshingPromise) return refreshingPromise;

    const now = Date.now();
    if (now - lastRefreshTime < MIN_REFRESH_INTERVAL) {
      return;
    }

    if (router.currentRoute.value.path.startsWith("/auth/")) {
      return;
    }

    bc?.postMessage({ type: "refresh-start" });
    refreshingPromise = refreshToken()
      .then(() => {
        console.log("✅ Token refreshed");
        lastRefreshTime = Date.now();
        bc?.postMessage({ type: "refresh-done" });
      })
      .catch((err) => {
        console.error("❌ Refresh failed", err);

        const status = err?.statusCode || err?.status || err?.response?.status;

        if (status === 401 || status === 403) {
          authStore.clearAuth();
          bc?.postMessage({ type: "logout" });
          if (!router.currentRoute.value.path.startsWith("/auth/")) {
            router.push({
              path: "/auth/login",
              query: { redirectTo: router.currentRoute.value.fullPath },
            });
          }
        }
      })
      .finally(() => {
        refreshingPromise = null;
      });

    return refreshingPromise;
  }

  // Загружаем профиль только если его НЕТ (не был загружен на сервере)
  async function boot() {
    // Если профиль уже загружен на SSR, пропускаем
    if (authStore.isAuthenticated) {
      console.log("✅ [Client] User already loaded from SSR");
      lastRefreshTime = Date.now();
      return;
    }

    console.log("⚠️ [Client Plugin] No user from SSR, loading on client...");

    // Пытаемся загрузить профиль на клиенте (для SPA-навигации)
    try {
      authStore.setLoading(true);
      const user = await getProfile();
      authStore.setUser(user);
      lastRefreshTime = Date.now();
      console.log("✅ [Client] User loaded:", user.username);
    } catch (err) {
      console.log("❌ [Client] Failed to load user");
      authStore.clearAuth();
    } finally {
      authStore.setLoading(false);
    }
  }

  function schedule() {
    clear();
    intervalId = window.setInterval(() => {
      if (document.hidden) return;
      safeRefresh();
    }, 14 * 60 * 1000);
  }

  function clear() {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = undefined;
    }
  }

  function onFocus() {
    if (!authStore.isAuthenticated) return;

    const now = Date.now();
    if (now - lastRefreshTime > 5 * 60 * 1000) {
      safeRefresh();
    }
  }

  window.addEventListener("focus", onFocus);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) onFocus();
  });
  window.addEventListener("beforeunload", () => {
    clear();
    bc?.close();
  });

  await boot();
  schedule();
  console.log("🏁 [Client Plugin] auth.client.ts FINISHED");
});
