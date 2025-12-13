import type { Submission, SubmissionDetail, Grade } from "~/types";

interface SubmissionsListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Submission[];
}

interface CreateSubmissionData {
  assignment: number | string;
  content: string;
  files?: File[];
}

interface UpdateSubmissionData {
  content?: string;
  files?: File[];
}

/**
 * Service для работы со сдачами заданий
 */
export const useSubmissionsService = () => {
  const api = useApi();

  /**
   * Получить список сдач (для учителя)
   */
  const getSubmissions = (filters?: {
    assignment?: number;
    course?: string;
    status?: string;
  }) => {
    return api.get<SubmissionsListResponse>("/submissions/", filters);
  };

  /**
   * Получить детали сдачи
   */
  const getSubmission = (id: number | string) => {
    return api.get<SubmissionDetail>(`/submissions/${id}/`);
  };

  /**
   * Создать сдачу задания
   */
  const createSubmission = async (
    data: CreateSubmissionData
  ): Promise<SubmissionDetail> => {
    const formData = new FormData();
    formData.append("assignment", String(data.assignment));
    formData.append("content", data.content);

    if (data.files) {
      data.files.forEach((file, index) => {
        formData.append(`files[${index}]`, file);
      });
    }

    return await api.fetch<SubmissionDetail>("/submissions/", {
      method: "POST",
      body: formData,
    });
  };

  /**
   * Обновить сдачу
   */
  const updateSubmission = async (
    id: number | string,
    data: UpdateSubmissionData
  ): Promise<SubmissionDetail> => {
    const formData = new FormData();
    if (data.content !== undefined) {
      formData.append("content", data.content);
    }

    if (data.files) {
      data.files.forEach((file, index) => {
        formData.append(`files[${index}]`, file);
      });
    }

    return await api.fetch<SubmissionDetail>(`/submissions/${id}/`, {
      method: "PATCH",
      body: formData,
    });
  };

  /**
   * Получить оценку за сдачу
   */
  const getGrade = async (
    submissionId: number | string
  ): Promise<Grade | null> => {
    try {
      return await api.get<Grade>(`/submissions/${submissionId}/grade/`);
    } catch {
      return null;
    }
  };

  return {
    getSubmissions,
    getSubmission,
    createSubmission,
    updateSubmission,
    getGrade,
  };
};
