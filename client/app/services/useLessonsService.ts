import type {
  Lesson,
  LessonDetail,
  LessonNavigation,
  LessonProgress,
  MarkLessonCompleteResponse,
} from "~/types";

interface LessonsListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Lesson[];
}

interface LessonViewResponse {
  lesson: LessonDetail;
  navigation: LessonNavigation;
  progress: LessonProgress | null;
  is_enrolled: boolean;
}

interface CreateLessonPayload {
  course: string; // slug
  title: string;
  slug?: string;
  description?: string;
  order?: number;
  duration_minutes?: number;
  is_published?: boolean;
  video_url?: string;
  content?: string;
}

interface UpdateLessonPayload {
  title?: string;
  slug?: string;
  description?: string;
  order?: number;
  duration_minutes?: number;
  is_published?: boolean;
  video_url?: string;
  content?: string;
}

/**
 * Service для работы с уроками
 * Отвечает за HTTP-запросы к API уроков
 */
export const useLessonsService = () => {
  const api = useApi();

  /**
   * Получить список уроков курса
   */
  const getLessonsByCourse = (courseSlug: string) => {
    return api.get<LessonsListResponse>("/lessons/", { course: courseSlug });
  };

  /**
   * Создать новый урок
   */
  const createLesson = (payload: CreateLessonPayload) => {
    return api.post<Lesson>("/lessons/", payload);
  };

  /**
   * Обновить урок
   */
  const updateLesson = (lessonSlug: string, payload: UpdateLessonPayload) => {
    return api.patch<Lesson>(`/lessons/${lessonSlug}/`, payload);
  };

  /**
   * Удалить урок
   */
  const deleteLesson = (lessonSlug: string) => {
    return api.delete<void>(`/lessons/${lessonSlug}/`);
  };

  /**
   * Получить детали урока по slug
   * Включает курс, материалы и контент
   */
  const getLessonBySlug = (courseSlug: string, lessonSlug: string) => {
    return api.get<LessonDetail>(`/lessons/${lessonSlug}/`);
  };

  /**
   * Получить полные данные для страницы урока
   * Включает навигацию и прогресс
   */
  // const getLessonView = (courseSlug: string, lessonSlug: string) => {
  //   return api.get<LessonViewResponse>(`/lessons/${lessonSlug}/view/`, {
  //     course: courseSlug,
  //   });
  // };

  /**
   * Отметить урок как просмотренный/завершённый
   */
  const markLessonComplete = (lessonSlug: string) => {
    return api.post<MarkLessonCompleteResponse>(
      `/lessons/${lessonSlug}/complete/`
    );
  };

  /**
   * Получить прогресс по уроку
   */
  const getLessonProgress = (lessonSlug: string) => {
    return api.get<LessonProgress>(`/lessons/${lessonSlug}/progress/`);
  };

  /**
   * Обновить прогресс просмотра видео
   */
  const updateVideoProgress = (lessonSlug: string, progressPercent: number) => {
    return api.post<{ success: boolean }>(
      `/lessons/${lessonSlug}/video-progress/`,
      {
        progress_percent: progressPercent,
      }
    );
  };

  /**
   * Получить навигацию по урокам курса
   */
  const getLessonNavigation = (courseSlug: string, lessonSlug: string) => {
    return api.get<LessonNavigation>(`/lessons/${lessonSlug}/navigation/`, {
      course: courseSlug,
    });
  };

  return {
    getLessonsByCourse,
    createLesson,
    updateLesson,
    deleteLesson,
    getLessonBySlug,
    // getLessonView,
    markLessonComplete,
    getLessonProgress,
    updateVideoProgress,
    getLessonNavigation,
  };
};
