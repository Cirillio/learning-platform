import type {
  Feedback,
  CreateFeedbackInput,
  FeedbackType,
  FeedbackStatus,
} from "~/schemas/feedback.schema";

export const feedbackService = () => {
  const { post, get } = useApi();

  /**
   * Создать новый фидбек
   */
  const createFeedback = async (
    data: CreateFeedbackInput
  ): Promise<Feedback> => {
    const formData = new FormData();
    formData.append("feedback_type", data.feedback_type);
    formData.append("title", data.title);
    formData.append("description", data.description);

    if (data.screenshot) {
      formData.append("screenshot", data.screenshot);
    }

    return post<Feedback>("/core/feedback/", formData);
  };

  /**
   * Получить список своих фидбеков
   */
  const getFeedbacks = async (params?: {
    type?: FeedbackType;
    status?: FeedbackStatus;
  }): Promise<Feedback[]> => {
    return get<Feedback[]>("/core/feedback/", params);
  };

  /**
   * Получить детали фидбека по ID
   */
  const getFeedbackById = async (id: number): Promise<Feedback> => {
    return get<Feedback>(`/core/feedback/${id}/`);
  };

  return {
    createFeedback,
    getFeedbacks,
    getFeedbackById,
  };
};
