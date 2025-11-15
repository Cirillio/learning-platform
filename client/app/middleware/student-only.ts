import type { User } from "~/types";

/**
 * Student-only middleware
 * Protects routes that require student role
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

  // Check if user is student
  if (!authStore.isStudent) {
    return navigateTo("/dashboard");
  }
});
