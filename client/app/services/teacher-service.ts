import type {
  Course,
  CourseDetail,
  Lesson,
  Assignment,
  Submission,
  Grade,
  CourseStudent,
} from "~/types";

interface CoursesListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Course[];
}

interface LessonsListResponse {
  count: number;
  results: Lesson[];
}

interface AssignmentsListResponse {
  count: number;
  results: Assignment[];
}

interface SubmissionsListResponse {
  count: number;
  results: Submission[];
}

interface StudentsListResponse {
  count: number;
  results: CourseStudent[];
}

interface CreateCourseData {
  title: string;
  short_description: string;
  description: string;
  category: number;
  difficulty: "beginner" | "intermediate" | "advanced";
  duration_weeks?: number | null;
  max_students?: number | null;
  status?: "draft" | "published";
  cover_image?: File;
}

interface CreateLessonData {
  course: string; // slug
  title: string;
  description?: string;
  content?: string;
  order?: number;
  duration_minutes?: number;
  video_url?: string;
  is_published?: boolean;
}

interface CreateAssignmentData {
  lesson: string; // slug
  title: string;
  description?: string;
  instructions?: string;
  max_score?: number;
  due_date?: string;
  is_required?: boolean;
  allow_late_submission?: boolean;
}

interface GradeSubmissionData {
  score: number;
  feedback?: string;
}

/**
 * Service для работы с функциями учителя
 */
export const teacherService = () => {
  const api = useApi();
  const authStore = useAuthStore();

  // --- Courses ---

  /**
   * Получить курсы текущего учителя
   */
  const getMyCourses = () => {
    return api.get<CoursesListResponse>("/courses/", {
      teacher: authStore.user?.id,
    });
  };

  /**
   * Создать курс
   */
  const createCourse = async (
    data: CreateCourseData
  ): Promise<CourseDetail> => {
    const formData = new FormData();

    Object.entries(data).forEach(([key, value]) => {
      if (value !== null && value !== undefined) {
        if (key === "cover_image" && value instanceof File) {
          formData.append(key, value);
        } else {
          formData.append(key, String(value));
        }
      }
    });

    return await api.fetch<CourseDetail>("/courses/", {
      method: "POST",
      body: formData,
    });
  };

  /**
   * Обновить курс
   */
  const updateCourse = async (
    slug: string,
    data: Partial<CreateCourseData>
  ): Promise<CourseDetail> => {
    const formData = new FormData();

    Object.entries(data).forEach(([key, value]) => {
      if (value !== null && value !== undefined) {
        if (key === "cover_image" && value instanceof File) {
          formData.append(key, value);
        } else {
          formData.append(key, String(value));
        }
      }
    });

    return await api.fetch<CourseDetail>(`/courses/${slug}/`, {
      method: "PATCH",
      body: formData,
    });
  };

  /**
   * Удалить курс
   */
  const deleteCourse = (slug: string) => {
    return api.delete(`/courses/${slug}/`);
  };

  // --- Lessons ---

  /**
   * Получить уроки курса
   */
  const getCourseLessons = (courseSlug: string) => {
    return api.get<LessonsListResponse>("/lessons/", { course: courseSlug });
  };

  /**
   * Создать урок
   */
  const createLesson = (data: CreateLessonData) => {
    return api.post<Lesson>("/lessons/", data);
  };

  /**
   * Обновить урок
   */
  const updateLesson = (slug: string, data: Partial<CreateLessonData>) => {
    return api.patch<Lesson>(`/lessons/${slug}/`, data);
  };

  /**
   * Удалить урок
   */
  const deleteLesson = (lessonId: number) => {
    return api.delete(`/lessons/${lessonId}/`);
  };

  // --- Assignments ---

  /**
   * Получить задания курса
   */
  const getCourseAssignments = (courseSlug: string) => {
    return api.get<AssignmentsListResponse>("/assignments/", {
      course: courseSlug,
    });
  };

  /**
   * Создать задание
   */
  const createAssignment = (data: CreateAssignmentData) => {
    return api.post<Assignment>("/assignments/", data);
  };

  /**
   * Обновить задание
   */
  const updateAssignment = (
    id: number,
    data: Partial<CreateAssignmentData>
  ) => {
    return api.patch<Assignment>(`/assignments/${id}/`, data);
  };

  /**
   * Удалить задание
   */
  const deleteAssignment = (id: number) => {
    return api.delete(`/assignments/${id}/`);
  };

  // --- Submissions & Grading ---

  /**
   * Получить сдачи для проверки
   */
  const getSubmissions = (filters?: {
    status?: string;
    assignment?: number;
    course?: string;
  }) => {
    return api.get<SubmissionsListResponse>("/submissions/", filters);
  };

  /**
   * Получить детали сдачи
   */
  const getSubmissionDetail = (id: number | string) => {
    return api.get<Submission>(`/submissions/${id}/`);
  };

  /**
   * Выставить оценку
   */
  const gradeSubmission = (
    submissionId: number | string,
    data: GradeSubmissionData
  ) => {
    return api.post<Grade>(`/submissions/${submissionId}/grade/`, data);
  };

  // --- Students ---

  /**
   * Получить студентов курса
   */
  const getCourseStudents = (courseSlug: string) => {
    return api.get<StudentsListResponse>(`/courses/${courseSlug}/students/`);
  };

  return {
    // Courses
    getMyCourses,
    createCourse,
    updateCourse,
    deleteCourse,

    // Lessons
    getCourseLessons,
    createLesson,
    updateLesson,
    deleteLesson,

    // Assignments
    getCourseAssignments,
    createAssignment,
    updateAssignment,
    deleteAssignment,

    // Submissions
    getSubmissions,
    getSubmissionDetail,
    gradeSubmission,

    // Students
    getCourseStudents,
  };
};
