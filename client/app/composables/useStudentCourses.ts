// composables/useStudentCourses.ts
import type { Course, CoursesResponse } from "~/types";
import { coursesService } from "../services/courses-service";

interface UseStudentCoursesReturn {
  courses: Ref<Course[]>;
  enrolledIds: Ref<Set<number>>;
  isEnrolled: (course: Course | number | string) => boolean;
  pending: Ref<boolean>;
  error: Ref<any>;
  refresh: () => Promise<void>;
  total: Ref<number>;
  isHydrated: Ref<boolean>; // 🆕 флаг гидратации
}

export function useStudentCourses(): UseStudentCoursesReturn {
  const coursesApi = coursesService();
  const { isAuthenticated, isStudent } = useAuthStore();

  const data = ref<CoursesResponse | null>(null);
  const pending = ref(false);
  const error = ref<any>(null);
  const isHydrated = ref(false); // 🆕 показывает, что данные загружены

  const courses = computed<Course[]>(() => {
    if (!data.value) return [];
    if (Array.isArray(data.value)) return data.value;
    return data.value.results || [];
  });

  const total = computed<number>(() => {
    if (!data.value) return 0;
    if (Array.isArray(data.value)) return data.value.length;
    return data.value.count || 0;
  });

  const enrolledIds = computed(() => new Set(courses.value.map((c) => c.id)));

  function isEnrolled(course: Course | number | string): boolean {
    if (!courses.value.length) return false;
    if (typeof course === "number") return enrolledIds.value.has(course);
    if (typeof course === "string") {
      return courses.value.some((c) => c.slug === course);
    }
    return enrolledIds.value.has(course.id);
  }

  async function refresh(): Promise<void> {
    // Грузим только если авторизован И студент
    if (!isAuthenticated || !isStudent) {
      isHydrated.value = true; // помечаем как "загружено", но данных нет
      return;
    }

    pending.value = true;
    error.value = null;

    try {
      data.value = await coursesApi.getMyCourses();
    } catch (err: any) {
      error.value = err;
      console.error("Failed to load student courses:", err);
    } finally {
      pending.value = false;
      isHydrated.value = true; // данные загружены (даже если ошибка)
    }
  }

  onMounted(() => {
    refresh();
  });

  return {
    courses,
    enrolledIds,
    isEnrolled,
    pending,
    error,
    total,
    refresh,
    isHydrated, // 🆕 экспортируем флаг
  };
}
