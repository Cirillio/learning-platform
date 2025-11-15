import type { User } from "~/types";
import { defineStore } from "pinia";

/**
 * Auth store using Pinia
 * Manages authentication state across the application
 * Tokens stored in HttpOnly cookies on backend - NOT in this store
 */
export const useAuthStore = defineStore("auth", () => {
  // State - ТОЛЬКО user, токенов нет!
  const user = ref<User | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const isAuthenticated = computed(() => !!user.value);
  const isTeacher = computed(() => user.value?.role === "teacher");
  const isStudent = computed(() => user.value?.role === "student");
  const userRole = computed(() => user.value?.role || null);

  // Actions
  const setUser = (userData: User | null): void => {
    user.value = userData;
  };

  const clearAuth = (): void => {
    user.value = null;
    error.value = null;
  };

  const setLoading = (loading: boolean): void => {
    isLoading.value = loading;
  };

  const setError = (errorMessage: string | null): void => {
    error.value = errorMessage;
  };

  return {
    // State
    user: readonly(user),
    isLoading: readonly(isLoading),
    error: readonly(error),

    // Getters
    isAuthenticated,
    isTeacher,
    isStudent,
    userRole,

    // Actions
    setUser,
    clearAuth,
    setLoading,
    setError,
  };
});
