import type { Assignment, Submission, SubmissionDetail, Grade } from "~/types";
import { assignmentsService, submissionsService } from "~/services";

interface UseAssignmentsOptions {
  courseSlug?: string;
  lessonSlug?: string;
}

/**
 * Composable для работы с заданиями студента
 */
export const useAssignments = (options: UseAssignmentsOptions = {}) => {
  const assignmentsApi = assignmentsService();
  const submissionsApi = submissionsService();
  const toast = useToast();

  // State
  const assignments = ref<Assignment[]>([]);
  const currentAssignment = ref<Assignment | null>(null);
  const currentSubmission = ref<SubmissionDetail | null>(null);
  const currentGrade = ref<Grade | null>(null);

  const isLoading = ref(false);
  const isSubmitting = ref(false);
  const error = ref<Error | null>(null);

  // Computed
  const hasSubmission = computed(() => !!currentSubmission.value);
  const isGraded = computed(() => currentSubmission.value?.status === "graded");
  const isPending = computed(
    () => currentSubmission.value?.status === "pending"
  );

  // Actions
  const fetchAssignments = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await assignmentsApi.getAssignments({
        course: options.courseSlug,
        lesson: options.lessonSlug,
      });
      assignments.value = response.results;
    } catch (e) {
      error.value = e as Error;
      console.error("Failed to fetch assignments:", e);
    } finally {
      isLoading.value = false;
    }
  };

  const fetchAssignment = async (id: number | string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const [assignment, submission] = await Promise.all([
        assignmentsApi.getAssignment(id),
        assignmentsApi.getMySubmission(id),
      ]);

      currentAssignment.value = assignment;
      currentSubmission.value = submission;

      // Fetch grade if submitted
      if (submission?.status === "graded") {
        currentGrade.value = await submissionsApi.getGrade(submission.id);
      }
    } catch (e) {
      error.value = e as Error;
      console.error("Failed to fetch assignment:", e);
    } finally {
      isLoading.value = false;
    }
  };

  const submitAssignment = async (
    assignmentId: number | string,
    content: string,
    files?: File[]
  ) => {
    isSubmitting.value = true;
    error.value = null;

    try {
      if (currentSubmission.value) {
        // Update existing
        currentSubmission.value = await submissionsApi.updateSubmission(
          currentSubmission.value.id,
          { content, files }
        );
        toast.add({
          title: "Ответ обновлён",
          color: "success",
          icon: "i-lucide-check",
        });
      } else {
        // Create new
        currentSubmission.value = await submissionsApi.createSubmission({
          assignment: assignmentId,
          content,
          files,
        });
        toast.add({
          title: "Задание сдано!",
          description: "Ожидайте проверки преподавателем",
          color: "success",
          icon: "i-lucide-check-circle",
        });
      }
    } catch (e: any) {
      error.value = e;
      toast.add({
        title: "Ошибка",
        description: e.data?.detail || "Не удалось отправить ответ",
        color: "error",
        icon: "i-lucide-alert-circle",
      });
      throw e;
    } finally {
      isSubmitting.value = false;
    }
  };

  const reset = () => {
    currentAssignment.value = null;
    currentSubmission.value = null;
    currentGrade.value = null;
    error.value = null;
  };

  return {
    // State
    assignments: readonly(assignments),
    currentAssignment: readonly(currentAssignment),
    currentSubmission: readonly(currentSubmission),
    currentGrade: readonly(currentGrade),
    isLoading: readonly(isLoading),
    isSubmitting: readonly(isSubmitting),
    error: readonly(error),

    // Computed
    hasSubmission,
    isGraded,
    isPending,

    // Actions
    fetchAssignments,
    fetchAssignment,
    submitAssignment,
    reset,
  };
};
