import type { Assignment, Submission, SubmissionDetail } from "~/types";

interface AssignmentsListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Assignment[];
}

interface AssignmentFilters {
  course?: string;
  lesson?: string;
  is_required?: boolean;
}

/**
 * Service для работы с заданиями
 */
export const useAssignmentsService = () => {
  const api = useApi();

  /**
   * Получить список заданий
   */
  const getAssignments = (filters?: AssignmentFilters) => {
    return api.get<AssignmentsListResponse>("/assignments/", filters);
  };

  /**
   * Получить задание по ID
   */
  const getAssignment = (id: number | string) => {
    return api.get<Assignment>(`/assignments/${id}/`);
  };

  /**
   * Получить задания урока
   */
  const getLessonAssignments = (lessonSlug: string) => {
    return api.get<AssignmentsListResponse>("/assignments/", {
      lesson: lessonSlug,
    });
  };

  /**
   * Получить мою сдачу задания
   */
  const getMySubmission = async (
    assignmentId: number | string
  ): Promise<SubmissionDetail | null> => {
    try {
      return await api.get<SubmissionDetail>(
        `/assignments/${assignmentId}/my-submission/`
      );
    } catch {
      return null;
    }
  };

  return {
    getAssignments,
    getAssignment,
    getLessonAssignments,
    getMySubmission,
  };
};
