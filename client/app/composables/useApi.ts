import type { User, LoginResponse } from "~/types";

export interface LoginRequest {
  username: string;
  password: string;
  remember_me?: boolean;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  role: "teacher" | "student";
  remember_me?: boolean;
}

// Мьютекс для refresh
let refreshingPromise: Promise<void> | null = null;

/**
 * API client composable
 * Uses HttpOnly cookies for authentication (managed by backend)
 * @returns API methods
 */
export const useApi = () => {
  const config = useRuntimeConfig();
  const baseURL = config.public.apiBase;

  const api = $fetch.create({
    baseURL,
    credentials: "include", // Для отправки httpOnly cookies
    headers: {
      "Content-Type": "application/json",
    },

    async onResponseError({ request, options, response }) {
      console.log(
        "⚠️ [API] Response error:",
        response.status,
        request.toString()
      );

      const requestUrl = request.toString();
      // Эндпоинты, для которых 401 - это ожидаемый ответ, а не повод для обновления токена
      const excludedEndpoints = [
        "/auth/login/",
        "/auth/register/",
        "/auth/refresh/",
      ];

      // Запускаем обновление только если статус 401 и запрос не в списке исключений
      if (
        response.status === 401 &&
        !excludedEndpoints.some(endpoint => requestUrl.includes(endpoint))
      ) {
        console.log("🔄 [API] 401 detected, attempting auto-refresh...");
        // Защита от параллельных refresh
        if (!refreshingPromise) {
          console.log("🚀 [API] This request is the FIRST to trigger the refresh.");
          refreshingPromise = $fetch("/auth/refresh/", {
            method: "POST",
            baseURL,
            credentials: "include",
          })
            .then(() => {
              console.log("✅ [API] Auto-refresh successful. Waiting requests can now proceed.");
              refreshingPromise = null;
            })
            .catch((err) => {
              console.error("❌ [API] Auto-refresh failed. This is the error that caused the logout.");
              // Логируем всю ошибку, чтобы увидеть статус и тело ответа от /auth/refresh/
              console.error("❌ [API] ДЕТАЛИ ОШИБКИ ОБНОВЛЕНИЯ:", JSON.stringify(err, null, 2));

              refreshingPromise = null;
              // Refresh провалился — разлогиниваем
              const authStore = useAuthStore();
              authStore.clearAuth();
              navigateTo("/auth/login");
              throw err;
            });
        } else {
          console.log("⏳ [API] Another request is already refreshing the token. Waiting...");
        }

        // Ждём завершения refresh
        await refreshingPromise;

        // Повторяем исходный запрос с обновлённым токеном
        console.log(`🔄 [API] Retrying original request: ${request.toString()}`);
        return $fetch(request, options as any);
      }
    },
  });

  const login = async (credentials: LoginRequest): Promise<LoginResponse> => {
    console.log("🔍 [API] Login request:", credentials);
    return await api("/auth/login/", {
      method: "POST",
      body: credentials,
    });
  };

  const register = async (userData: RegisterRequest): Promise<void> => {
    return await api("/auth/register/", {
      method: "POST",
      body: userData,
    });
  };

  const refreshToken = async (): Promise<void> => {
    console.log("🔄 [API] Refreshing token...");
    try {
      await $fetch("/auth/refresh/", {
        method: "POST",
        baseURL,
        credentials: "include",
      });
      console.log("✅ [API] Token refreshed successfully");
    } catch (error: any) {
      console.error("❌ [API] Refresh failed:", error);
      const statusCode =
        error?.status || error?.statusCode || error?.response?.status || 500;
      console.error("❌ [API] Refresh status:", statusCode);
      throw {
        statusCode,
        status: statusCode,
        message: error?.data?.message || error?.message || "Refresh failed",
        data: error?.data,
      };
    }
  };

  const removeToken = async (): Promise<void> => {
    // Прямой вызов без интерсептора
    await $fetch("/auth/logout/", {
      method: "POST",
      baseURL,
      credentials: "include",
    });
  };

  const getProfile = async (): Promise<User> => {
    return await api("/auth/profile/", {
      method: "GET",
      credentials: "include",
    });
  };

  const updateProfile = async (profileData: Partial<User>): Promise<User> => {
    return await api("/auth/profile/", {
      method: "PATCH",
      body: profileData,
    });
  };

  return {
    login,
    register,
    refreshToken,
    removeToken,
    getProfile,
    updateProfile,
  };
};
