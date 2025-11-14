/**
 * Teacher-only middleware
 * Protects routes that require teacher role
 */
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    return navigateTo("/auth/login");
  }

  // Check if user is teacher
  if (!authStore.isTeacher) {
    return navigateTo("/dashboard");
  }
});
