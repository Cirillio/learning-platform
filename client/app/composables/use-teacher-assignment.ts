import type { Assignment, LessonDetail, SubmissionsResponse } from "~/types";
import { useApi, useToast } from "#imports";

export const useTeacherAssignment = () => {
  const route = useRoute();
  const router = useRouter();
  const api = useApi();
  const toast = useToast();

  const courseSlug = computed(() => route.params.slug as string);
  const assignmentId = computed(() => route.params.id as string);

  // --- Data Fetching ---

  // 1. Fetch Assignment
  const { data: assignment, status: assignmentStatus } =
    useAsyncData<Assignment>(
      `teacher-assignment-${assignmentId.value}`,
      () => api.get<Assignment>(`/assignments/${assignmentId.value}/`)
    );

  // 2. Fetch Linked Lesson
  const { data: lesson } = useAsyncData<LessonDetail | null>(
    `teacher-assignment-lesson-${assignmentId.value}`,
    async () => {
      if (!assignment.value?.lesson) return null;
      try {
        return await api.get<LessonDetail>(
          `/lessons/${assignment.value.lesson}/`
        );
      } catch {
        return null;
      }
    },
    { watch: [assignment] }
  );

  // 3. Fetch Submissions
  const { data: submissionsData, refresh: refreshSubmissions } =
    useAsyncData<SubmissionsResponse>(
      `teacher-assignment-submissions-${assignmentId.value}`,
      () =>
        api.get<SubmissionsResponse>("/submissions/", {
          assignment: assignmentId.value,
        })
    );

  const submissions = computed(() => submissionsData.value?.results || []);

  // --- Computed Logic ---

  const pendingCount = computed(
    () => submissions.value.filter((s) => s.status === "pending").length
  );

  const gradedCount = computed(
    () => submissions.value.filter((s) => s.status === "graded").length
  );

  const lateCount = computed(
    () => submissions.value.filter((s) => s.is_late).length
  );

  const isDueDatePassed = computed(() => {
    if (!assignment.value?.due_date) return false;
    return new Date(assignment.value.due_date) < new Date();
  });

  // --- Actions ---

  const handleDelete = async () => {
    if (
      !confirm(
        "Вы уверены, что хотите удалить это задание? Все сдачи студентов также будут удалены."
      )
    )
      return;

    try {
      await api.delete(`/assignments/${assignmentId.value}/`);
      toast.add({ title: "Задание удалено", color: "success" });
      router.push(`/teacher/courses/${courseSlug.value}/assignments`);
    } catch (e) {
      toast.add({
        title: "Ошибка удаления",
        description: (e as Error).message,
        color: "error",
      });
    }
  };

  return {
    // State
    courseSlug,
    assignmentId,
    assignment,
    assignmentStatus,
    lesson,
    submissions,
    
    // Computed
    pendingCount,
    gradedCount,
    lateCount,
    isDueDatePassed,

    // Actions
    handleDelete,
    refreshSubmissions,
  };
};
