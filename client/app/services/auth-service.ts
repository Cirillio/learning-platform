import type {
  AuthResponse,
  LoginCredentials,
  RegisterCredentials,
  UserProfile,
  User,
} from "~/types";
import { normalizeUser } from "~/utils/get-user-from-profile";

export const authService = () => {
  const api = useApi();

  const login = (credentials: LoginCredentials) => {
    return api.post<AuthResponse>("/auth/login/", credentials);
  };

  const register = (credentials: RegisterCredentials) => {
    return api.post("/auth/register/", credentials);
  };

  const logout = () => {
    return api.post("/auth/logout/");
  };

  const refreshToken = () => {
    return api.post("/auth/refresh/");
  };

  const fetchUser = async (): Promise<User> => {
    const raw = await api.get<UserProfile>("/auth/profile/");
    return normalizeUser(raw);
  };

  return {
    login,
    register,
    logout,
    refreshToken,
    fetchUser,
  };
};
