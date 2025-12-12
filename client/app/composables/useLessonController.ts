import type {
  Lesson,
  LessonDetail,
  LessonNavigation,
  LessonProgress,
  LessonCompletionStatus,
} from "~/types";
import { useLessonsService } from "~/services";

interface UseLessonControllerOptions {
  courseSlug: string;
  lessonSlug: string;
}

/**
 * Composable для управления состоянием урока
 * Централизованная бизнес-логика для Lesson View
 */
export const useLessonController = (options: UseLessonControllerOptions) => {
  const { courseSlug, lessonSlug } = options;
  const lessonsService = useLessonsService();
  const toast = useToast();
  const router = useRouter();

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------
  const lesson = ref<LessonDetail | null>(null);
  const navigation = ref<LessonNavigation | null>(null);
  const progress = ref<LessonProgress | null>(null);
  const allLessons = ref<Lesson[]>([]);

  const isLoading = ref(true);
  const isCompletingLesson = ref(false);
  const error = ref<Error | null>(null);
  const isEnrolled = ref(false);

  // ---------------------------------------------------------------------------
  // Computed
  // ---------------------------------------------------------------------------
  const completionStatus = computed<LessonCompletionStatus>(() => {
    if (!progress.value) return "not_started";
    return progress.value.status;
  });

  const isCompleted = computed(() => completionStatus.value === "completed");

  const progressPercent = computed(() => {
    if (!progress.value) return 0;
    return progress.value.progress_percent;
  });

  const hasVideo = computed(() => Boolean(lesson.value?.video_url));

  const hasMaterials = computed(
    () => lesson.value?.materials && lesson.value.materials.length > 0
  );

  const hasAssignments = computed(
    () => lesson.value?.assignments_count && lesson.value.assignments_count > 0
  );

  const canNavigatePrevious = computed(() =>
    Boolean(navigation.value?.previous)
  );
  const canNavigateNext = computed(() => Boolean(navigation.value?.next));

  const breadcrumbs = computed(() => {
    if (!lesson.value) return [];
    return [
      { label: "Курсы", to: "/courses", icon: "i-lucide-graduation-cap" },
      {
        label: lesson.value.course.title,
        to: `/courses/${lesson.value.course.slug}`,
      },
      {
        label: lesson.value.title,
        to: `/courses/${lesson.value.course.slug}/lessons/${lesson.value.slug}`,
      },
    ];
  });

  // ---------------------------------------------------------------------------
  // Actions
  // ---------------------------------------------------------------------------

  /**
   * Загрузить данные урока
   */
  const fetchLesson = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      // Параллельная загрузка данных для оптимизации
      const [lessonData, lessonsListData] = await Promise.all([
        lessonsService.getLessonBySlug(courseSlug, lessonSlug),
        lessonsService.getLessonsByCourse(courseSlug),
      ]);

      lesson.value = lessonData;
      allLessons.value = lessonsListData.results || [];

      // Вычисляем навигацию на клиенте
      computeNavigation();

      // Пробуем загрузить прогресс (может не быть если не записан)
      try {
        progress.value = await lessonsService.getLessonProgress(lessonSlug);
      } catch {
        // Прогресс недоступен - пользователь не записан или нет прогресса
        progress.value = null;
      }
    } catch (e) {
      error.value = e as Error;
      console.error("Failed to fetch lesson:", e);
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Вычислить навигацию на основе списка уроков
   */
  const computeNavigation = () => {
    if (!allLessons.value.length || !lesson.value) {
      navigation.value = null;
      return;
    }

    const sortedLessons = [...allLessons.value].sort(
      (a, b) => a.order - b.order
    );
    const currentIndex = sortedLessons.findIndex((l) => l.slug === lessonSlug);

    if (currentIndex === -1) {
      navigation.value = null;
      return;
    }

    const prevLesson =
      currentIndex > 0 ? sortedLessons[currentIndex - 1] : null;
    const nextLesson =
      currentIndex < sortedLessons.length - 1
        ? sortedLessons[currentIndex + 1]
        : null;

    navigation.value = {
      previous: prevLesson
        ? {
            id: prevLesson.id,
            slug: prevLesson.slug,
            title: prevLesson.title,
            order: prevLesson.order,
          }
        : null,
      next: nextLesson
        ? {
            id: nextLesson.id,
            slug: nextLesson.slug,
            title: nextLesson.title,
            order: nextLesson.order,
          }
        : null,
      current_index: currentIndex,
      total_lessons: sortedLessons.length,
    };
  };

  /**
   * Отметить урок как завершённый
   */
  const markAsComplete = async () => {
    if (isCompleted.value || isCompletingLesson.value) return;

    isCompletingLesson.value = true;

    try {
      const response = await lessonsService.markLessonComplete(lessonSlug);

      if (response.success) {
        progress.value = response.progress;
        toast.add({
          title: "Урок завершён!",
          description: "Отличная работа! Переходите к следующему уроку.",
          color: "success",
          icon: "i-lucide-check-circle",
        });
      }
    } catch (e) {
      toast.add({
        title: "Ошибка",
        description: "Не удалось отметить урок как завершённый",
        color: "error",
        icon: "i-lucide-alert-circle",
      });
      console.error("Failed to mark lesson complete:", e);
    } finally {
      isCompletingLesson.value = false;
    }
  };

  /**
   * Навигация к предыдущему уроку
   */
  const goToPreviousLesson = () => {
    if (!canNavigatePrevious.value || !navigation.value?.previous) return;
    router.push(
      `/courses/${courseSlug}/lessons/${navigation.value.previous.slug}`
    );
  };

  /**
   * Навигация к следующему уроку
   */
  const goToNextLesson = () => {
    if (!canNavigateNext.value || !navigation.value?.next) return;
    router.push(`/courses/${courseSlug}/lessons/${navigation.value.next.slug}`);
  };

  /**
   * Обновить прогресс просмотра видео
   */
  const updateVideoProgress = async (percent: number) => {
    try {
      await lessonsService.updateVideoProgress(lessonSlug, percent);

      // Обновляем локальный прогресс
      if (progress.value) {
        progress.value.progress_percent = percent;
        if (percent >= 90 && progress.value.status !== "completed") {
          progress.value.status = "in_progress";
        }
      }
    } catch (e) {
      console.error("Failed to update video progress:", e);
    }
  };

  // ---------------------------------------------------------------------------
  // Lifecycle
  // ---------------------------------------------------------------------------
  // Авто-загрузка при создании
  onMounted(() => {
    fetchLesson();
  });

  // Следим за изменением slug урока
  watch(
    () => options.lessonSlug,
    (newSlug) => {
      if (newSlug !== lessonSlug) {
        fetchLesson();
      }
    }
  );

  return {
    // State
    lesson,
    navigation,
    progress,
    allLessons,
    isLoading,
    isCompletingLesson,
    error,
    isEnrolled,

    // Computed
    completionStatus,
    isCompleted,
    progressPercent,
    hasVideo,
    hasMaterials,
    hasAssignments,
    canNavigatePrevious,
    canNavigateNext,
    breadcrumbs,

    // Actions
    fetchLesson,
    markAsComplete,
    goToPreviousLesson,
    goToNextLesson,
    updateVideoProgress,
  };
};
