import type { LoginCredentials, RegisterCredentials } from "~/types";
import { authService } from "~/services/auth-service";

/**
 * Composable for authentication operations
 * Uses Pinia store for state management (Single Responsibility Principle)
 * @returns Authentication methods and computed state
 */
export const useAuth = () => {
  const authStore = useAuthStore();
  const authApi = authService();

  const login = async (credentials: LoginCredentials) => {
    authStore.setLoading(true);
    try {
      const response = await authApi.login(credentials);
      authStore.setUser(response.user);

      await navigateTo("/profile");
    } catch (error: any) {
      authStore.setError(
        error.data?.error || "Login failed. Please try again."
      );
      throw error;
    } finally {
      authStore.setLoading(false);
    }
  };

  const register = async (credentials: RegisterCredentials) => {
    authStore.setLoading(true);
    try {
      await authApi.register(credentials);
      await login({
        username: credentials.username,
        password: credentials.password,
        remember_me: true,
      });
    } catch (error: any) {
      authStore.setError(
        error.data?.error || "Registration failed. Please try again."
      );
      throw error;
    } finally {
      authStore.setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
    } catch {}

    authStore.clearAuth();
  };

  const fetchUser = async () => {
    try {
      const user = await authApi.fetchUser();
      authStore.setUser(user);
    } catch (error) {
      authStore.clearAuth();
    }
  };

  return {
    user: computed(() => authStore.user),
    isAuthenticated: computed(() => authStore.isAuthenticated),
    isLoading: computed(() => authStore.isLoading),
    error: computed(() => authStore.error),
    login,
    register,
    logout,
    fetchUser,
  };
};
