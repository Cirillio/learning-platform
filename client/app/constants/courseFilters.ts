/**
 * Constants for course filters and pagination
 * Centralized default values to ensure consistency across the application
 */

/**
 * Default page size for courses pagination
 * This value matches the backend default page size
 */
export const COURSE_PAGE_SIZE_DEFAULT = 6;

/**
 * Default ordering for courses
 * Courses are ordered by creation date descending by default
 */
export const COURSE_ORDERING_DEFAULT = "-created_at";

/**
 * Minimum page size for courses pagination
 */
export const COURSE_PAGE_SIZE_MIN = 6;

/**
 * Maximum page size for courses pagination
 */
export const COURSE_PAGE_SIZE_MAX = 50;

/**
 * Default search placeholder text
 */
export const COURSE_SEARCH_PLACEHOLDER = "Поиск курсов...";

/**
 * Cache key prefix for courses data
 */
export const COURSE_CACHE_KEY_PREFIX = "courses";

/**
 * Default filter options for course filters
 */
export const COURSE_FILTER_DEFAULTS = {
  pageSize: COURSE_PAGE_SIZE_DEFAULT,
  defaultOrdering: COURSE_ORDERING_DEFAULT,
  search: "",
  category: undefined,
  difficulty: undefined,
  ordering: COURSE_ORDERING_DEFAULT,
  page: 1,
} as const;
