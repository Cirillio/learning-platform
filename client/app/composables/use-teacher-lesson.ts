import type { LessonDetail, Assignment, Submission, AssignmentsResponse, SubmissionsResponse } from "~/types";
import { useApi, useToast } from "#imports";
import { formatDate } from "~/utils/formatters.util";

export const useTeacherLesson = () => {
  const route = useRoute();
  const router = useRouter();
  const api = useApi();
  const toast = useToast();

  const courseSlug = computed(() => route.params.slug as string);
  const lessonSlug = computed(() => route.params.lesson_slug as string);

  // --- Data Fetching ---

  // 1. Fetch Lesson
  const { data: lesson, status: lessonStatus } = useAsyncData<LessonDetail>(
    `teacher-lesson-${lessonSlug.value}`,
    () => api.get<LessonDetail>(`/lessons/${lessonSlug.value}/`)
  );

  // 2. Fetch Assignments
  const { data: assignmentsData } =
    useAsyncData<AssignmentsResponse>(
      `teacher-lesson-assignments-${lessonSlug.value}`,
      () =>
        api.get<AssignmentsResponse>("/assignments/", {
          lesson: lessonSlug.value,
        })
    );

  const assignments = computed(() => assignmentsData.value?.results || []);

  // 3. Fetch Submissions (Waterfall: wait for assignments)
  const { data: submissionsData } = useAsyncData<SubmissionsResponse>(
    `teacher-lesson-submissions-${lessonSlug.value}`,
    async () => {
      // Return empty if no assignments
      if (assignments.value.length === 0) {
        return { count: 0, results: [] } as any; // Cast to avoid strict type issues if type mismatch
      }

      // Parallel fetch for all assignments
      const submissionsPromises = assignments.value.map((assignment) =>
        api.get<SubmissionsResponse>("/submissions/", {
          assignment: assignment.id.toString(),
        })
      );

      const submissionsResults = await Promise.all(submissionsPromises);

      // Merge results
      const allSubmissions = submissionsResults.flatMap((res) => res.results);

      // Return pseudo-paginated response structure
      return {
        count: allSubmissions.length,
        results: allSubmissions,
        next: null,
        previous: null
      };
    },
    { watch: [assignments] }
  );

  const submissions = computed(() => submissionsData.value?.results || []);

  // --- Computed Logic ---

  // Group submissions by assignment ID
  const submissionsByAssignment = computed(() => {
    const grouped: Record<number, Submission[]> = {};
    for (const sub of submissions.value) {
      const assignmentId = sub.assignment;
      if (!grouped[assignmentId]) {
        grouped[assignmentId] = [];
      }
      grouped[assignmentId]!.push(sub);
    }
    return grouped;
  });

  const pendingSubmissions = computed(
    () => submissions.value.filter((s) => s.status === "pending").length
  );

  const gradedSubmissions = computed(
    () => submissions.value.filter((s) => s.status === "graded").length
  );

  // --- Actions ---

  const handleDelete = async () => {
    if (
      !confirm(
        "Вы уверены, что хотите удалить этот урок? Все материалы и задания также будут удалены."
      )
    )
      return;

    try {
      await api.delete(`/lessons/${lessonSlug.value}/`);
      toast.add({ title: "Урок удален", color: "success" });
      router.push(`/teacher/courses/${courseSlug.value}/lessons`);
    } catch (e) {
      toast.add({
        title: "Ошибка удаления",
        description: (e as Error).message,
        color: "error",
      });
    }
  };

  return {
    courseSlug,
    lessonSlug,
    lesson,
    lessonStatus,
    assignments,
    submissions,
    submissionsByAssignment,
    pendingSubmissions,
    gradedSubmissions,
    handleDelete
  };
};
