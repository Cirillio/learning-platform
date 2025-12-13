import type {
  Course,
  CourseDetail,
  Lesson,
  Assignment,
  Submission,
  Grade,
} from "~/types";
import { useTeacherService } from "~/services";

/**
 * Composable для панели управления учителя
 * Предоставляет централизованный доступ к данным и действиям учителя
 */
export const useTeacher = () => {
  const teacherService = useTeacherService();
  const authStore = useAuthStore();
  const toast = useToast();

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------
  const courses = ref<Course[]>([]);
  const currentCourse = ref<CourseDetail | null>(null);
  const lessons = ref<Lesson[]>([]);
  const assignments = ref<Assignment[]>([]);
  const submissions = ref<Submission[]>([]);

  const isLoading = ref(false);
  const error = ref<Error | null>(null);

  // ---------------------------------------------------------------------------
  // Computed
  // ---------------------------------------------------------------------------
  const isTeacher = computed(() => authStore.isTeacher);

  const totalStudents = computed(() =>
    courses.value.reduce((acc, course) => acc + (course.enrolled_count || 0), 0)
  );

  const pendingSubmissionsCount = computed(
    () => submissions.value.filter((s) => s.status === "pending").length
  );

  const publishedCoursesCount = computed(
    () => courses.value.filter((c) => c.status === "published").length
  );

  // ---------------------------------------------------------------------------
  // Actions: Courses
  // ---------------------------------------------------------------------------
  const fetchMyCourses = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await teacherService.getMyCourses();
      courses.value = response.results;
    } catch (e) {
      error.value = e as Error;
      console.error("Failed to fetch courses:", e);
    } finally {
      isLoading.value = false;
    }
  };

  const createCourse = async (
    data: Parameters<typeof teacherService.createCourse>[0]
  ) => {
    try {
      const course = await teacherService.createCourse(data);
      toast.add({
        title: "Курс создан",
        color: "success",
      });
      await fetchMyCourses();
      return course;
    } catch (e: any) {
      toast.add({
        title: "Ошибка",
        description: e.data?.detail || "Не удалось создать курс",
        color: "error",
      });
      throw e;
    }
  };

  const deleteCourse = async (slug: string) => {
    try {
      await teacherService.deleteCourse(slug);
      toast.add({
        title: "Курс удалён",
        color: "success",
      });
      await fetchMyCourses();
    } catch (e: any) {
      toast.add({
        title: "Ошибка",
        description: e.data?.detail || "Не удалось удалить курс",
        color: "error",
      });
      throw e;
    }
  };

  // ---------------------------------------------------------------------------
  // Actions: Lessons
  // ---------------------------------------------------------------------------
  const fetchCourseLessons = async (courseSlug: string) => {
    try {
      const response = await teacherService.getCourseLessons(courseSlug);
      lessons.value = response.results;
    } catch (e) {
      console.error("Failed to fetch lessons:", e);
    }
  };

  const createLesson = async (
    data: Parameters<typeof teacherService.createLesson>[0]
  ) => {
    try {
      const lesson = await teacherService.createLesson(data);
      toast.add({
        title: "Урок создан",
        color: "success",
      });
      if (data.course) {
        await fetchCourseLessons(data.course);
      }
      return lesson;
    } catch (e: any) {
      toast.add({
        title: "Ошибка",
        description: e.data?.detail || "Не удалось создать урок",
        color: "error",
      });
      throw e;
    }
  };

  const deleteLesson = async (lessonId: number, courseSlug: string) => {
    try {
      await teacherService.deleteLesson(lessonId);
      toast.add({
        title: "Урок удалён",
        color: "success",
      });
      await fetchCourseLessons(courseSlug);
    } catch (e: any) {
      toast.add({
        title: "Ошибка",
        description: e.data?.detail || "Не удалось удалить урок",
        color: "error",
      });
      throw e;
    }
  };

  // ---------------------------------------------------------------------------
  // Actions: Assignments
  // ---------------------------------------------------------------------------
  const fetchCourseAssignments = async (courseSlug: string) => {
    try {
      const response = await teacherService.getCourseAssignments(courseSlug);
      assignments.value = response.results;
    } catch (e) {
      console.error("Failed to fetch assignments:", e);
    }
  };

  const createAssignment = async (
    data: Parameters<typeof teacherService.createAssignment>[0]
  ) => {
    try {
      const assignment = await teacherService.createAssignment(data);
      toast.add({
        title: "Задание создано",
        color: "success",
      });
      return assignment;
    } catch (e: any) {
      toast.add({
        title: "Ошибка",
        description: e.data?.detail || "Не удалось создать задание",
        color: "error",
      });
      throw e;
    }
  };

  // ---------------------------------------------------------------------------
  // Actions: Grading
  // ---------------------------------------------------------------------------
  const fetchPendingSubmissions = async () => {
    try {
      const response = await teacherService.getSubmissions({
        status: "pending",
      });
      submissions.value = response.results;
    } catch (e) {
      console.error("Failed to fetch submissions:", e);
    }
  };

  const gradeSubmission = async (
    submissionId: number | string,
    data: { score: number; feedback?: string }
  ) => {
    try {
      const grade = await teacherService.gradeSubmission(submissionId, data);
      toast.add({
        title: "Оценка выставлена",
        color: "success",
      });
      await fetchPendingSubmissions();
      return grade;
    } catch (e: any) {
      toast.add({
        title: "Ошибка",
        description: e.data?.detail || "Не удалось выставить оценку",
        color: "error",
      });
      throw e;
    }
  };

  // ---------------------------------------------------------------------------
  // Dashboard Stats
  // ---------------------------------------------------------------------------
  const fetchDashboardData = async () => {
    isLoading.value = true;
    try {
      await Promise.all([fetchMyCourses(), fetchPendingSubmissions()]);
    } finally {
      isLoading.value = false;
    }
  };

  return {
    // State
    courses: readonly(courses),
    currentCourse: readonly(currentCourse),
    lessons: readonly(lessons),
    assignments: readonly(assignments),
    submissions: readonly(submissions),
    isLoading: readonly(isLoading),
    error: readonly(error),

    // Computed
    isTeacher,
    totalStudents,
    pendingSubmissionsCount,
    publishedCoursesCount,

    // Courses
    fetchMyCourses,
    createCourse,
    deleteCourse,

    // Lessons
    fetchCourseLessons,
    createLesson,
    deleteLesson,

    // Assignments
    fetchCourseAssignments,
    createAssignment,

    // Grading
    fetchPendingSubmissions,
    gradeSubmission,

    // Dashboard
    fetchDashboardData,
  };
};
