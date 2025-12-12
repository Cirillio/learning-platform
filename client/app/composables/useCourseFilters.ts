import { reactive, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import type { CourseFilters } from "~/types";
import {
  COURSE_PAGE_SIZE_DEFAULT,
  COURSE_ORDERING_DEFAULT,
} from "~/constants/courseFilters";

/**
 * Simplified composable for managing course filters.
 * - State is the single source of truth.
 * - URL is synced from state.
 * - State is initialized from URL (SSR friendly).
 */
export function useCourseFilters() {
  const route = useRoute();
  const router = useRouter();

  // 1. Initialize state from URL (SSR friendly)
  const filters = reactive({
    search: (route.query.search as string) || "",
    category: (route.query.category as string) || undefined,
    difficulty: (route.query.difficulty as string) || undefined,
    ordering: (route.query.ordering as string) || COURSE_ORDERING_DEFAULT,
    page: Number(route.query.page) || 1,
  });

  // 2. Computed API params (clean for API calls)
  const apiParams = computed<CourseFilters>(() => {
    const params: CourseFilters = {
      page: filters.page,
      page_size: COURSE_PAGE_SIZE_DEFAULT,
    };

    if (filters.search) params.search = filters.search;
    if (filters.category) params.category = filters.category;
    if (filters.difficulty) params.difficulty = filters.difficulty;
    if (filters.ordering) params.ordering = filters.ordering;

    return params;
  });

  // 3. Sync State -> URL
  watch(
    filters,
    () => {
      const query: Record<string, any> = { ...filters };

      // Remove defaults/empty to keep URL clean
      if (!query.search) delete query.search;
      if (!query.category) delete query.category;
      if (!query.difficulty) delete query.difficulty;
      if (query.ordering === COURSE_ORDERING_DEFAULT) delete query.ordering;
      if (query.page === 1) delete query.page;

      router.push({ query });
    },
    { deep: true }
  );

  // 4. Sync URL -> State (Handle Back/Forward navigation)
  watch(
    () => route.query,
    (newQuery) => {
      // Only update if values differ to avoid loops
      if (newQuery.search !== filters.search)
        filters.search = (newQuery.search as string) || "";
      if (newQuery.category !== filters.category)
        filters.category = (newQuery.category as string) || undefined;
      if (newQuery.difficulty !== filters.difficulty)
        filters.difficulty = (newQuery.difficulty as string) || undefined;
      if (newQuery.ordering !== filters.ordering)
        filters.ordering =
          (newQuery.ordering as string) || COURSE_ORDERING_DEFAULT;
      if (Number(newQuery.page || 1) !== filters.page)
        filters.page = Number(newQuery.page) || 1;
    }
  );

  // 5. Helper methods
  const setFilter = (key: keyof typeof filters, value: any) => {
    if (key !== "page") {
      filters.page = 1; // Reset page on filter change
    }
    // @ts-ignore
    filters[key] = value;
  };

  const resetFilters = () => {
    filters.search = "";
    filters.category = undefined;
    filters.difficulty = undefined;
    filters.ordering = COURSE_ORDERING_DEFAULT;
    filters.page = 1;
  };

  return {
    filters,
    apiParams,
    setFilter,
    resetFilters,
  };
}
