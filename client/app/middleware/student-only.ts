/**
 * Student-only middleware
 * Protects routes that require student role
 */
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    return navigateTo("/auth/login");
  }

  // Check if user is student
  if (!authStore.isStudent) {
    return navigateTo("/dashboard");
  }
});
