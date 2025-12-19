import type { CreateFeedbackInput } from "~/schemas/feedback.schema";

/**
 * Composable для работы с системой фидбека
 * Упрощает отправку обратной связи с клиентской стороны
 */
export const useFeedback = () => {
  const { createFeedback } = feedbackService();
  const toast = useToast();

  const isSubmitting = ref(false);

  /**
   * Быстрая отправка фидбека с автоматической обработкой ошибок
   */
  const submitFeedback = async (data: CreateFeedbackInput) => {
    try {
      isSubmitting.value = true;

      await createFeedback(data);

      toast.add({
        title: "Спасибо за отзыв!",
        description: "Мы обязательно рассмотрим ваше обращение",
        color: "success",
      });

      return { success: true };
    } catch (error: any) {
      toast.add({
        title: "Ошибка отправки",
        description: error.message || "Не удалось отправить отзыв",
        color: "error",
      });

      return { success: false, error };
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    submitFeedback,
    isSubmitting: readonly(isSubmitting),
  };
};
