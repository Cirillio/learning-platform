export interface LoginCredentials {
  username: string;
  password: string;
  remember_me?: boolean;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  role: "teacher" | "student";
  remember_me?: boolean;
}

/**
 * Composable for authentication operations
 * Uses Pinia store for state management (Single Responsibility Principle)
 * @returns Authentication methods and computed state
 */
export const useAuth = () => {
  const authStore = useAuthStore();
  const { login: apiLogin, register: apiRegister, removeToken } = useApi();

  const login = async (credentials: LoginCredentials) => {
    console.log("🔍 [Auth] Login credentials:", credentials);
    authStore.setLoading(true);
    try {
      const response = await apiLogin(credentials);
      authStore.setUser(response.user);

      await navigateTo("/dashboard");
    } catch (error: any) {
      authStore.setError(error.data?.error || "Login failed");
      throw error;
    } finally {
      authStore.setLoading(false);
    }
  };

  const register = async (userData: RegisterData) => {
    authStore.setLoading(true);
    try {
      await apiRegister(userData);
      await login({
        username: userData.username,
        password: userData.password,
        remember_me: userData.remember_me,
      });
    } catch (error: any) {
      authStore.setError(error.data?.error || "Registration failed");
      throw error;
    } finally {
      authStore.setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await removeToken();
    } catch {}

    authStore.clearAuth();

    await navigateTo("/auth/login");
  };

  return {
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated,
    isLoading: authStore.isLoading,
    error: authStore.error,
    login,
    register,
    logout,
  };
};
