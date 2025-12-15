import type { User } from "~/types";

/**
 * Teacher-only middleware
 * Protects routes that require teacher role
 */
export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore();

  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    return navigateTo({
      path: "/auth/login",
      query: { redirectTo: to.fullPath },
    });
  }

  // Check if user is teacher
  if (!authStore.isTeacher) {
    return navigateTo("/learning");
  }
});
