import { useCoursesService } from "~/services";

/**
 * Middleware для проверки записи на курс
 * Проверяет, что пользователь записан на курс перед доступом к уроку
 */
export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore();

  // Сначала проверяем авторизацию
  if (!authStore.isAuthenticated) {
    return navigateTo({
      path: "/auth/login",
      query: { redirectTo: to.fullPath },
    });
  }

  // Получаем slug курса из роута (поддержка обоих вариантов)
  const courseSlug = (to.params.course_slug || to.params.slug) as string;

  if (!courseSlug) {
    return navigateTo("/courses");
  }

  try {
    const coursesService = useCoursesService();
    const course = await coursesService.getCourse(courseSlug);

    // Проверяем, записан ли пользователь на курс
    if (!course.is_enrolled) {
      // Редиректим на страницу курса для записи
      return navigateTo({
        path: `/courses/${courseSlug}`,
        query: { error: "not_enrolled" },
      });
    }
  } catch (error) {
    // Курс не найден или ошибка API
    console.error("Failed to check enrollment:", error);
    return navigateTo("/courses");
  }
});
