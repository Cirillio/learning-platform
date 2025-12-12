import type { FetchOptions } from "ofetch";
import { useAuthStore } from "~/stores/auth";

// Мьютекс для refresh
let refreshingPromise: Promise<void> | null = null;

/**
 * API клиент с удобными методами
 * Отвечает за HTTP запросы и автоматический refresh токенов
 */
export const useApi = () => {
  const config = useRuntimeConfig();
  const authStore = useAuthStore();

  // Headers management for SSR
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Accept: "application/json",
  };

  if (import.meta.server) {
    const event = useRequestEvent();
    const cookieHeader = event?.node.req.headers.cookie;
    if (cookieHeader) {
      headers["Cookie"] = cookieHeader;
    }
  }

  // Создаем базовый fetch с обработкой ошибок
  const api = $fetch.create({
    baseURL: config.public.apiBase,
    credentials: "include",
    headers,

    async onResponseError({ request, options, response }) {
      // Эндпоинты, для которых 401 - это ожидаемый ответ
      const excludedEndpoints = [
        "/auth/login/",
        "/auth/register/",
        "/auth/refresh/",
      ];

      const requestUrl = request.toString();
      const isExcluded = excludedEndpoints.some((endpoint) =>
        requestUrl.includes(endpoint)
      );

      if (response.status === 401 && !isExcluded) {
        if (!refreshingPromise) {
          refreshingPromise = $fetch("/auth/refresh/", {
            method: "POST",
            baseURL: config.public.apiBase,
            credentials: "include",
          })
            .then(() => {
              refreshingPromise = null;
            })
            .catch((err) => {
              refreshingPromise = null;
              authStore.clearAuth();
              if (import.meta.client) {
                navigateTo("/auth/login");
              }
              throw err;
            });
        }

        await refreshingPromise;
        return $fetch(request, options as any);
      }
    },
  });

  // Удобные методы
  const get = <T>(url: string, params?: any) =>
    api<T>(url, { method: "GET", query: params });
  const post = <T>(url: string, body?: any) =>
    api<T>(url, { method: "POST", body });
  const patch = <T>(url: string, body?: any) =>
    api<T>(url, { method: "PATCH", body });
  const put = <T>(url: string, body?: any) =>
    api<T>(url, { method: "PUT", body });
  const del = <T>(url: string) => api<T>(url, { method: "DELETE" });

  return {
    get,
    post,
    patch,
    put,
    delete: del,
    fetch: api, // raw access if needed
  };
};
