import type { User } from "~/types";

export interface LoginCredentials {
  username: string;
  password: string;
  remember?: boolean;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  role: "teacher" | "student";
}

/**
 * Composable for authentication operations
 * Uses Pinia store for state management (Single Responsibility Principle)
 * @returns Authentication methods and computed state
 */
export const useAuth = () => {
  const authStore = useAuthStore();
  const {
    login: apiLogin,
    register: apiRegister,
    getProfile,
    updateProfile,
  } = useApi();

  /**
   * Login user with credentials
   * @param credentials - Username, password, and remember option
   */
  const login = async (credentials: LoginCredentials): Promise<void> => {
    authStore.setLoading(true);
    authStore.setError(null);

    const response = await apiLogin(credentials);

    authStore.setTokens(response.tokens.access, response.tokens.refresh);
    authStore.setUser(response.user);

    authStore.setLoading(false);

    await navigateTo("/dashboard");
  };

  /**
   * Register new user
   * @param userData - Registration data
   */
  const register = async (userData: RegisterData): Promise<void> => {
    authStore.setLoading(true);
    authStore.setError(null);

    await apiRegister(userData);

    // Auto-login after registration
    await login({
      username: userData.username,
      password: userData.password,
    });

    authStore.setLoading(false);
  };

  /**
   * Logout current user
   */
  const logout = async (): Promise<void> => {
    authStore.clearAuth();
    await navigateTo("/auth/login");
  };

  /**
   * Load user profile from API
   */
  const loadProfile = async (): Promise<void> => {
    if (!authStore.isAuthenticated) return;

    const profile = await getProfile();
    authStore.setUser(profile);
  };

  /**
   * Update user profile
   * @param profileData - Partial user data to update
   */
  const updateUserProfile = async (
    profileData: Partial<User>
  ): Promise<void> => {
    authStore.setLoading(true);
    authStore.setError(null);

    const updatedUser = await updateProfile(profileData);
    authStore.setUser(updatedUser);

    authStore.setLoading(false);
  };

  return {
    // State from store
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated,
    isLoading: authStore.isLoading,
    error: authStore.error,
    isTeacher: authStore.isTeacher,
    isStudent: authStore.isStudent,

    // Methods
    login,
    register,
    logout,
    loadProfile,
    updateUserProfile,
  };
};
