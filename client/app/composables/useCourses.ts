import { useAsyncData } from "#app";
import { unref, onUnmounted, type Ref, type ComputedRef } from "vue";
import type {
  Category,
  Course,
  CourseDetail,
  FilterOption,
  CourseFilterGroup,
  CourseFilters,
  CoursesResponse,
  CategoriesResponse,
  EnrollResponse,
  UnenrollResponse,
  PaginationParams,
} from "~/types";

export const useCourses = () => {
  const { api } = useApi();

  /**
   * Получение списка курсов с поддержкой SSR.
   * @param params - Реактивный объект с параметрами для фильтрации и поиска.
   */
  const getCourses = (
    params: Ref<CourseFilters> | ComputedRef<CourseFilters>
  ) => {
    // Создаем уникальный ключ на основе параметров для правильного кэширования
    const cacheKey = computed(() => {
      const p = unref(params);
      const key = `courses-${p.page || 1}-${p.page_size || 10}-${
        p.search || ""
      }-${p.category || ""}-${p.difficulty || ""}-${p.ordering || ""}`;
      return key;
    });
    return useAsyncData<CoursesResponse>(cacheKey, () =>
      api("/courses", {
        method: "GET",
        params: unref(params),
      })
    );
  };

  /**
   * Получение детальной информации о курсе с поддержкой SSR.
   * @param slug - Слаг курса.
   */
  const getCourse = (slug: string) => {
    return useAsyncData<CourseDetail>(`course-${slug}`, () =>
      api(`/courses/${slug}/`, {
        method: "GET",
      })
    );
  };

  /**
   * Получение детальной информации о категории.
   * @param slug - Слаг категории.
   */
  const getCategory = (slug: string) => {
    return useAsyncData<Category>(`category-${slug}`, () =>
      api(`/categories/${slug}/`, {
        method: "GET",
      })
    );
  };

  /**
   * Получение списка курсов текущего пользователя (мои курсы).
   * КЛИЕНТСКИЙ запрос (без SSR) — данные персональные, требуют авторизации.
   * Запрос будет автоматически отменен при размонтировании компонента.
   */
  const getMyCourses = () => {
    const controller = new AbortController();

    onUnmounted(() => {
      controller.abort();
    });

    return api<CoursesResponse>("/courses/my_courses/", {
      method: "GET",
      signal: controller.signal,
    });
  };

  /**
   * Получение списка категорий курсов с поддержкой SSR.
   */
  const getCategories = (options: { ordering?: string } & PaginationParams) => {
    return useAsyncData<CategoriesResponse>(
      `categories-${options.page || 1}-${options.page_size || 10}-${
        options.ordering || ""
      }`,
      () =>
        api("/categories/", {
          method: "GET",
          query: options,
        })
    );
  };

  /**
   * Получение списка уроков для конкретного курса.
   * @param slug - Слаг курса.
   */
  const getCourseLessons = (slug: string) => {
    return useAsyncData<any>(`course-${slug}-lessons`, () =>
      api(`/lessons/`, {
        method: "GET",
        params: { course: slug },
      })
    );
  };

  // --- Функции-действия (без useAsyncData) ---

  /**
   * Запись на курс.
   * @param slug - Слаг курса.
   */
  const enrollToCourse = async (
    slug: string
  ): Promise<
    { success: true; data: EnrollResponse } | { success: false; error: any }
  > => {
    try {
      const response = await api<EnrollResponse>(`/courses/${slug}/enroll/`, {
        method: "POST",
      });
      // После успешной записи можно, например, обновить данные о курсе
      // или перенаправить пользователя.
      // refreshNuxtData(`course-${slug}`); // Обновит данные для getCourse
      return { success: true, data: response };
    } catch (error) {
      console.error("Enrollment failed:", error);
      return { success: false, error };
    }
  };

  /**
   * Отмена записи на курс.
   * @param slug - Слаг курса.
   */
  const unenrollFromCourse = async (
    slug: string
  ): Promise<
    { success: true; data: UnenrollResponse } | { success: false; error: any }
  > => {
    try {
      const response = await api<UnenrollResponse>(
        `/courses/${slug}/unenroll/`,
        {
          method: "POST",
        }
      );
      // refreshNuxtData(`course-${slug}`); // Обновит данные
      return { success: true, data: response };
    } catch (error) {
      console.error("Unenrollment failed:", error);
      return { success: false, error };
    }
  };

  return {
    getCourses,
    getCourse,
    getCategory,
    getMyCourses,
    getCategories,
    getCourseLessons,
    enrollToCourse,
    unenrollFromCourse,
  };
};
