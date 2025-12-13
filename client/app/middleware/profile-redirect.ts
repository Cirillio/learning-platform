/**
 * Middleware для редиректа учителей на /teacher/profile
 * Используется на странице /profile для разделения ролей
 */
export default defineNuxtRouteMiddleware(() => {
  const { user, isAuthenticated } = useAuth();

  // Если не авторизован — middleware auth сделает редирект
  if (!isAuthenticated.value || !user.value) {
    return;
  }

  // Если учитель — редирект на teacher profile
  if (user.value.role === "teacher") {
    return navigateTo("/teacher", { replace: true });
  }
});
