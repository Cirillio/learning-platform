import type { User, AuthTokens, LoginResponse } from "~/types";

export interface LoginRequest {
  username: string;
  password: string;
  remember?: boolean;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  role: "teacher" | "student";
}

/**
 * API client composable
 * Provides methods for API interactions with automatic JWT token handling
 * @returns API methods
 */
export const useApi = () => {
  const config = useRuntimeConfig();
  const baseURL = config.public.apiBase;

  // Создаем экземпляр $fetch с базовой конфигурацией
  const api = $fetch.create({
    baseURL,
    headers: {
      "Content-Type": "application/json",
    },
    onRequest({ options }) {
      // Добавляем токен авторизации, если он есть
      const token = useCookie("auth_token");
      if (token.value) {
        const headers = options.headers || {};
        if (headers instanceof Headers) {
          headers.set("Authorization", `Bearer ${token.value}`);
        } else {
          (
            headers as Record<string, string>
          ).Authorization = `Bearer ${token.value}`;
          options.headers = headers;
        }
      }
    },
    onResponseError({ response }) {
      // Обработка ошибок API
      if (response.status === 401) {
        // Токен истек или недействителен
        useCookie("auth_token").value = null;
        useCookie("refresh_token").value = null;
        navigateTo("/auth/login");
      }
    },
  });

  // Методы для работы с API
  const login = async (credentials: LoginRequest): Promise<LoginResponse> => {
    return await api("/auth/login/", {
      method: "POST",
      body: credentials,
    });
  };

  const register = async (userData: RegisterRequest): Promise<User> => {
    return await api("/auth/register/", {
      method: "POST",
      body: userData,
    });
  };

  const refreshToken = async (): Promise<AuthTokens> => {
    const refresh = useCookie("refresh_token");
    const response = await api<{ access: string; refresh: string }>(
      "/token/refresh/",
      {
        method: "POST",
        body: { refresh: refresh.value },
      }
    );
    return {
      access: response.access,
      refresh: response.refresh,
    };
  };

  const getProfile = async (): Promise<User> => {
    return await api("/auth/profile/", {
      method: "GET",
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
    getProfile,
    updateProfile,
  };
};
