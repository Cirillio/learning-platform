/**
 * Owner middleware
 * Protects routes that require resource ownership
 * Can be extended to check specific resource ownership
 */
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    return navigateTo("/auth/login");
  }

  // Additional ownership checks can be added here
  // For example, checking if user owns a specific course/lesson
});
