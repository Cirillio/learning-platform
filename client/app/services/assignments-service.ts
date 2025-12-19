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

interface CreateAssignmentPayload {
  lesson: string; // slug
  title: string;
  description?: string;
  instructions?: string;
  max_score?: number;
  due_date?: string | null;
  is_required?: boolean;
  allow_late_submission?: boolean;
}

interface UpdateAssignmentPayload {
  lesson?: string;
  title?: string;
  description?: string;
  instructions?: string;
  max_score?: number;
  due_date?: string | null;
  is_required?: boolean;
  allow_late_submission?: boolean;
}

/**
 * Service для работы с заданиями
 */
export const assignmentsService = () => {
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
   * Создать задание
   */
  const createAssignment = (payload: CreateAssignmentPayload) => {
    return api.post<Assignment>("/assignments/", payload);
  };

  /**
   * Обновить задание
   */
  const updateAssignment = (
    id: number | string,
    payload: UpdateAssignmentPayload
  ) => {
    return api.patch<Assignment>(`/assignments/${id}/`, payload);
  };

  /**
   * Удалить задание
   */
  const deleteAssignment = (id: number | string) => {
    return api.delete<void>(`/assignments/${id}/`);
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
    createAssignment,
    updateAssignment,
    deleteAssignment,
    getLessonAssignments,
    getMySubmission,
  };
};
