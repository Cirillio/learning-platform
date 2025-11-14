import type { User } from "~/types";

/**
 * Auth store using Pinia
 * Manages authentication state across the application
 */
export const useAuthStore = defineStore("auth", () => {
  // State
  const user = ref<User | null>(null);
  const token = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value);
  const isTeacher = computed(() => user.value?.role === "teacher");
  const isStudent = computed(() => user.value?.role === "student");
  const userRole = computed(() => user.value?.role || null);

  // Actions
  const setUser = (userData: User | null): void => {
    user.value = userData;
  };

  const setTokens = (accessToken: string, refreshTokenValue: string): void => {
    token.value = accessToken;
    refreshToken.value = refreshTokenValue;

    // Store in cookies for persistence
    const authTokenCookie = useCookie("auth_token", {
      maxAge: 60 * 60 * 24 * 7, // 7 days
      sameSite: "lax",
      secure: process.env.NODE_ENV === "production",
    });
    const refreshTokenCookie = useCookie("refresh_token", {
      maxAge: 60 * 60 * 24 * 30, // 30 days
      sameSite: "lax",
      secure: process.env.NODE_ENV === "production",
    });

    authTokenCookie.value = accessToken;
    refreshTokenCookie.value = refreshTokenValue;
  };

  const clearAuth = (): void => {
    user.value = null;
    token.value = null;
    refreshToken.value = null;
    error.value = null;

    // Clear cookies
    const authTokenCookie = useCookie("auth_token");
    const refreshTokenCookie = useCookie("refresh_token");
    authTokenCookie.value = null;
    refreshTokenCookie.value = null;
  };

  const setLoading = (loading: boolean): void => {
    isLoading.value = loading;
  };

  const setError = (errorMessage: string | null): void => {
    error.value = errorMessage;
  };

  // Initialize from cookies on store creation
  const initAuth = (): void => {
    const savedToken = useCookie("auth_token");
    const savedRefreshToken = useCookie("refresh_token");

    if (savedToken.value && savedRefreshToken.value) {
      token.value = savedToken.value;
      refreshToken.value = savedRefreshToken.value;
      // User will be loaded separately when needed
    }
  };

  // Initialize auth state
  initAuth();

  return {
    // State
    user: readonly(user),
    token: readonly(token),
    refreshToken: readonly(refreshToken),
    isLoading: readonly(isLoading),
    error: readonly(error),

    // Getters
    isAuthenticated,
    isTeacher,
    isStudent,
    userRole,

    // Actions
    setUser,
    setTokens,
    clearAuth,
    setLoading,
    setError,
  };
});
