export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) {
    return navigateTo({
      path: "/auth/login",
      query: { redirectTo: to.fullPath },
    });
  }
});
