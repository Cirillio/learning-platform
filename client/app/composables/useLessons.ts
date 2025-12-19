import type { Lesson, LessonDetail } from "~/types";
import { lessonsService } from "~/services";

interface UseLessonsOptions {
  courseSlug: string;
}

interface CreateLessonPayload {
  course: string;
  title: string;
  slug?: string;
  description?: string;
  content?: string;
  order?: number;
  duration_minutes?: number;
  is_published?: boolean;
  video_url?: string;
}

interface UpdateLessonPayload {
  title?: string;
  slug?: string;
  description?: string;
  content?: string;
  order?: number;
  duration_minutes?: number;
  is_published?: boolean;
  video_url?: string;
}

/**
 * Composable для управления уроками преподавателем
 * CRUD операции с optimistic updates
 */
export const useLessons = (options: UseLessonsOptions) => {
  const { courseSlug } = options;
  const lessonsApi = lessonsService();
  const toast = useToast();

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------
  const lessons = ref<Lesson[]>([]);
  const currentLesson = ref<LessonDetail | null>(null);
  const isLoading = ref(false);
  const isCreating = ref(false);
  const isUpdating = ref(false);
  const isDeleting = ref(false);
  const error = ref<Error | null>(null);

  // ---------------------------------------------------------------------------
  // Computed
  // ---------------------------------------------------------------------------
  const sortedLessons = computed(() =>
    [...lessons.value].sort((a, b) => a.order - b.order)
  );

  const publishedLessons = computed(() =>
    lessons.value.filter((l) => l.is_published)
  );

  const draftLessons = computed(() =>
    lessons.value.filter((l) => !l.is_published)
  );

  const lessonsCount = computed(() => lessons.value.length);

  const nextOrder = computed(() => {
    if (lessons.value.length === 0) return 1;
    return Math.max(...lessons.value.map((l) => l.order)) + 1;
  });

  // ---------------------------------------------------------------------------
  // Actions: Fetch
  // ---------------------------------------------------------------------------
  const fetchLessons = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await lessonsApi.getLessonsByCourse(courseSlug);
      lessons.value = response.results;
    } catch (e) {
      error.value = e as Error;
      console.error("Failed to fetch lessons:", e);
      toast.add({
        title: "Ошибка",
        description: "Не удалось загрузить уроки",
        color: "error",
      });
    } finally {
      isLoading.value = false;
    }
  };

  const fetchLesson = async (lessonSlug: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await lessonsApi.getLessonView(
        courseSlug,
        lessonSlug
      );
      currentLesson.value = response.lesson;
      return response.lesson;
    } catch (e) {
      error.value = e as Error;
      console.error("Failed to fetch lesson:", e);
      toast.add({
        title: "Ошибка",
        description: "Не удалось загрузить урок",
        color: "error",
      });
      return null;
    } finally {
      isLoading.value = false;
    }
  };

  // ---------------------------------------------------------------------------
  // Actions: Create
  // ---------------------------------------------------------------------------
  const createLesson = async (payload: CreateLessonPayload) => {
    isCreating.value = true;
    error.value = null;

    // Optimistic: добавляем временный урок
    const tempId = Date.now();
    const tempLesson: Lesson = {
      id: tempId,
      course: courseSlug,
      title: payload.title,
      slug: payload.slug || "",
      description: payload.description || "",
      order: payload.order || nextOrder.value,
      duration_minutes: payload.duration_minutes || 0,
      is_published: payload.is_published || false,
      video_url: payload.video_url || null,
      materials_count: 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    lessons.value.push(tempLesson);

    try {
      const newLesson = await lessonsApi.createLesson({
        ...payload,
        course: courseSlug,
      });

      // Заменяем временный урок на реальный
      const index = lessons.value.findIndex((l) => l.id === tempId);
      if (index !== -1) {
        lessons.value[index] = newLesson;
      }

      toast.add({
        title: "Успешно",
        description: "Урок создан",
        color: "success",
      });

      return newLesson;
    } catch (e) {
      // Rollback
      lessons.value = lessons.value.filter((l) => l.id !== tempId);
      error.value = e as Error;
      console.error("Failed to create lesson:", e);
      toast.add({
        title: "Ошибка",
        description: "Не удалось создать урок",
        color: "error",
      });
      return null;
    } finally {
      isCreating.value = false;
    }
  };

  // ---------------------------------------------------------------------------
  // Actions: Update
  // ---------------------------------------------------------------------------
  const updateLesson = async (
    lessonSlug: string,
    payload: UpdateLessonPayload
  ) => {
    isUpdating.value = true;
    error.value = null;

    // Сохраняем старое состояние для rollback
    const index = lessons.value.findIndex((l) => l.slug === lessonSlug);
    const oldLesson = index !== -1 ? { ...lessons.value[index] } : null;

    // Optimistic update
    if (index !== -1) {
      lessons.value[index] = { ...lessons.value[index], ...payload } as Lesson;
    }

    try {
      const updatedLesson = await lessonsApi.updateLesson(
        lessonSlug,
        payload
      );

      // Обновляем с реальными данными
      if (index !== -1) {
        lessons.value[index] = updatedLesson;
      }

      // Обновляем currentLesson если это тот же урок
      if (currentLesson.value?.slug === lessonSlug) {
        Object.assign(currentLesson.value, updatedLesson);
      }

      toast.add({
        title: "Успешно",
        description: "Урок обновлен",
        color: "success",
      });

      return updatedLesson;
    } catch (e) {
      // Rollback
      if (oldLesson && index !== -1) {
        lessons.value[index] = oldLesson as Lesson;
      }
      error.value = e as Error;
      console.error("Failed to update lesson:", e);
      toast.add({
        title: "Ошибка",
        description: "Не удалось обновить урок",
        color: "error",
      });
      return null;
    } finally {
      isUpdating.value = false;
    }
  };

  // ---------------------------------------------------------------------------
  // Actions: Delete
  // ---------------------------------------------------------------------------
  const deleteLesson = async (lessonSlug: string) => {
    isDeleting.value = true;
    error.value = null;

    // Сохраняем для rollback
    const deletedLesson = lessons.value.find((l) => l.slug === lessonSlug);
    const deletedIndex = lessons.value.findIndex((l) => l.slug === lessonSlug);

    // Optimistic delete
    lessons.value = lessons.value.filter((l) => l.slug !== lessonSlug);

    try {
      await lessonsApi.deleteLesson(lessonSlug);

      // Очищаем currentLesson если удалили его
      if (currentLesson.value?.slug === lessonSlug) {
        currentLesson.value = null;
      }

      toast.add({
        title: "Успешно",
        description: "Урок удален",
        color: "success",
      });

      return true;
    } catch (e) {
      // Rollback
      if (deletedLesson && deletedIndex !== -1) {
        lessons.value.splice(deletedIndex, 0, deletedLesson);
      }
      error.value = e as Error;
      console.error("Failed to delete lesson:", e);
      toast.add({
        title: "Ошибка",
        description: "Не удалось удалить урок",
        color: "error",
      });
      return false;
    } finally {
      isDeleting.value = false;
    }
  };

  // ---------------------------------------------------------------------------
  // Actions: Reorder
  // ---------------------------------------------------------------------------
  const reorderLessons = async (lessonSlug: string, newOrder: number) => {
    const lesson = lessons.value.find((l) => l.slug === lessonSlug);
    if (!lesson) return false;

    const oldOrder = lesson.order;

    // Optimistic reorder
    lessons.value = lessons.value.map((l) => {
      if (l.slug === lessonSlug) {
        return { ...l, order: newOrder };
      }
      if (oldOrder < newOrder) {
        // Двигаем вниз - уменьшаем order промежуточных
        if (l.order > oldOrder && l.order <= newOrder) {
          return { ...l, order: l.order - 1 };
        }
      } else {
        // Двигаем вверх - увеличиваем order промежуточных
        if (l.order >= newOrder && l.order < oldOrder) {
          return { ...l, order: l.order + 1 };
        }
      }
      return l;
    });

    try {
      await lessonsApi.updateLesson(lessonSlug, { order: newOrder });
      return true;
    } catch (e) {
      // Rollback - перезагружаем уроки
      await fetchLessons();
      error.value = e as Error;
      toast.add({
        title: "Ошибка",
        description: "Не удалось изменить порядок",
        color: "error",
      });
      return false;
    }
  };

  // ---------------------------------------------------------------------------
  // Actions: Toggle Publish
  // ---------------------------------------------------------------------------
  const togglePublish = async (lessonSlug: string) => {
    const lesson = lessons.value.find((l) => l.slug === lessonSlug);
    if (!lesson) return false;

    const newStatus = !lesson.is_published;
    return await updateLesson(lessonSlug, { is_published: newStatus });
  };

  // ---------------------------------------------------------------------------
  // Utilities
  // ---------------------------------------------------------------------------
  const getLessonBySlug = (slug: string) =>
    lessons.value.find((l) => l.slug === slug);

  const reset = () => {
    lessons.value = [];
    currentLesson.value = null;
    error.value = null;
  };

  return {
    // State
    lessons,
    currentLesson,
    isLoading,
    isCreating,
    isUpdating,
    isDeleting,
    error,

    // Computed
    sortedLessons,
    publishedLessons,
    draftLessons,
    lessonsCount,
    nextOrder,

    // Actions
    fetchLessons,
    fetchLesson,
    createLesson,
    updateLesson,
    deleteLesson,
    reorderLessons,
    togglePublish,

    // Utilities
    getLessonBySlug,
    reset,
  };
};
