import { computed, type ComputedRef } from "vue";
import { useRoute, useRouter } from "vue-router";
import type {
  FilterOption,
  CourseFilters,
  CourseFiltersResponse,
} from "~/types";
import {
  COURSE_PAGE_SIZE_DEFAULT,
  COURSE_ORDERING_DEFAULT,
} from "~/constants/courseFilters";

interface UseCourseFiltersOptions {
  pageSize?: number;
  defaultOrdering?: string;
  filterOptions?: Ref<CourseFiltersResponse | null | undefined>;
}

interface UseCourseFiltersReturn {
  // Filter options data
  filterOptions?: Ref<CourseFiltersResponse | null | undefined>;
  categoryOptions: ComputedRef<FilterOption[]>;
  difficultyOptions: ComputedRef<FilterOption[]>;
  orderingOptions: ComputedRef<FilterOption[]>;

  // Computed values
  searchValue: ComputedRef<string>;
  selectedCategory: ComputedRef<FilterOption | undefined>;
  selectedDifficulty: ComputedRef<FilterOption | undefined>;
  selectedOrdering: ComputedRef<FilterOption | undefined>;
  currentPage: ComputedRef<number>;
  apiFilters: ComputedRef<CourseFilters>;

  // Update methods
  updateSearch: (value: string) => void;
  updateCategory: (option: string | undefined) => void;
  updateDifficulty: (option: string | undefined) => void;
  updateOrdering: (option: string | undefined) => void;
  updatePage: (page: number) => void;
  applyFilters: (filters: {
    search?: string;
    category?: string;
    difficulty?: string;
    ordering?: string;
  }) => void;
  resetFilters: () => void;
}

/**
 * Composable для управления фильтрами курсов
 *
 * Обрабатывает:
 * - Получение опций для фильтрации с сервера (SSR)
 * - Синхронизацию фильтров с URL query параметрами
 * - Преобразование между строками URL и объектами FilterOption
 * - Сброс страницы при изменении фильтров
 * - Подготовку параметров для API запросов
 *
 * @param options - Дополнительные настройки
 * @returns Реактивные значения фильтров и методы для их обновления
 */
export function useCourseFilters(
  options: UseCourseFiltersOptions = {}
): UseCourseFiltersReturn {
  const route = useRoute();
  const router = useRouter();

  const {
    pageSize = COURSE_PAGE_SIZE_DEFAULT,
    defaultOrdering = COURSE_ORDERING_DEFAULT,
    filterOptions,
  } = options;

  // ============================================================================
  // Получение опций фильтров с сервера (SSR)
  // ============================================================================

  // Подготавливаем опции для USelectMenu
  const categoryOptions = computed(
    () =>
      filterOptions?.value?.filters.find((f) => f.value === "category")
        ?.values || []
  );
  const difficultyOptions = computed(
    () =>
      filterOptions?.value?.filters.find((f) => f.value === "difficulty")
        ?.values || []
  );
  const orderingOptions = computed(
    () =>
      filterOptions?.value?.filters.find((f) => f.value === "ordering")
        ?.values || []
  );

  // ============================================================================
  // Вспомогательные функции
  // ============================================================================

  /**
   * Находит FilterOption по value из URL
   */
  function findFilterOption(
    options: FilterOption[],
    value: string
  ): FilterOption | undefined {
    return options.find((option) => option.value === value);
  }

  /**
   * Обновляет query параметры с сбросом страницы
   */
  function updateQuery(updates: Record<string, string | undefined>): void {
    router.push({
      query: {
        ...route.query,
        ...updates,
        page: "1", // Всегда сбрасываем на первую страницу при изменении фильтров
      },
    });
  }

  /**
   * Обновляет query параметры без сброса страницы (для пагинации)
   */
  function updateQueryWithoutReset(
    updates: Record<string, string | undefined>
  ): void {
    router.push({
      query: {
        ...route.query,
        ...updates,
      },
    });
  }

  // ============================================================================
  // Computed - текущие значения фильтров из URL
  // ============================================================================

  const searchValue = computed(() => String(route.query.search || ""));

  const selectedCategory = computed(() =>
    route.query.category
      ? findFilterOption(categoryOptions.value, String(route.query.category))
      : undefined
  );

  const selectedDifficulty = computed(() =>
    route.query.difficulty
      ? findFilterOption(
          difficultyOptions.value,
          String(route.query.difficulty)
        )
      : undefined
  );

  const selectedOrdering = computed(() => {
    const orderingValue = String(route.query.ordering || defaultOrdering);
    return findFilterOption(orderingOptions.value, orderingValue);
  });

  const currentPage = computed(() => Number(route.query.page || 1));

  /**
   * Параметры для API запроса (со строковыми значениями)
   */
  const apiFilters = computed<CourseFilters>(() => ({
    search: (route.query.search as string) || undefined,
    category: (route.query.category as string) || undefined,
    difficulty: (route.query.difficulty as string) || undefined,
    ordering: (route.query.ordering as string) || defaultOrdering,
    page: currentPage.value,
    page_size: pageSize,
  }));

  // ============================================================================
  // Методы обновления фильтров
  // ============================================================================

  function updateSearch(value: string): void {
    updateQuery({
      search: value || undefined,
    });
  }

  function updateCategory(option: string | undefined): void {
    updateQuery({
      category: option || undefined,
    });
  }

  function updateDifficulty(option: string | undefined): void {
    updateQuery({
      difficulty: option || undefined,
    });
  }

  function updateOrdering(option: string | undefined): void {
    updateQuery({
      ordering: option || undefined,
    });
  }

  function updatePage(page: number): void {
    updateQueryWithoutReset({
      page: String(page),
    });
  }

  /**
   * Применяет несколько фильтров одновременно
   */
  function applyFilters(filters: {
    search?: string;
    category?: string;
    difficulty?: string;
    ordering?: string;
  }): void {
    updateQuery({
      search: filters.search || undefined,
      category: filters.category || undefined,
      difficulty: filters.difficulty || undefined,
      ordering: filters.ordering || undefined,
    });
  }

  /**
   * Сбрасывает все фильтры к начальным значениям
   */
  function resetFilters(): void {
    router.push({
      query: {
        ordering: defaultOrdering,
        page: "1",
      },
    });
  }

  // ============================================================================
  // Return
  // ============================================================================

  return {
    // Filter options data
    filterOptions,
    categoryOptions,
    difficultyOptions,
    orderingOptions,

    // Computed values
    searchValue,
    selectedCategory,
    selectedDifficulty,
    selectedOrdering,
    currentPage,
    apiFilters,

    // Update methods
    updateSearch,
    updateCategory,
    updateDifficulty,
    updateOrdering,
    updatePage,
    applyFilters,
    resetFilters,
  };
}
