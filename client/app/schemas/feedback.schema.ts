import { z } from "zod";

export const feedbackTypeSchema = z.enum([
  "bug",
  "feature",
  "improvement",
  "question",
  "other",
]);

export const feedbackStatusSchema = z.enum([
  "new",
  "in_progress",
  "resolved",
  "closed",
]);

export const createFeedbackSchema = z.object({
  feedback_type: feedbackTypeSchema,
  title: z
    .string()
    .min(5, "Заголовок должен содержать минимум 5 символов")
    .max(200, "Заголовок слишком длинный"),
  description: z
    .string()
    .min(10, "Описание должно содержать минимум 10 символов")
    .max(2000, "Описание слишком длинное"),
  screenshot: z.instanceof(File).optional(),
});

export const feedbackSchema = createFeedbackSchema.extend({
  id: z.number(),
  user: z.number(),
  user_name: z.string(),
  user_email: z.string().email(),
  status: feedbackStatusSchema,
  priority: z.number().min(1).max(5),
  screenshot_url: z.string().url().nullable(),
  admin_response: z.string(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
  resolved_at: z.string().datetime().nullable(),
});

export type FeedbackType = z.infer<typeof feedbackTypeSchema>;
export type FeedbackStatus = z.infer<typeof feedbackStatusSchema>;
export type CreateFeedbackInput = z.infer<typeof createFeedbackSchema>;
export type Feedback = z.infer<typeof feedbackSchema>;

export const FEEDBACK_TYPE_LABELS: Record<FeedbackType, string> = {
  bug: "Ошибка/Баг",
  feature: "Новая функция",
  improvement: "Улучшение",
  question: "Вопрос",
  other: "Другое",
};

export const FEEDBACK_TYPE_ICONS: Record<FeedbackType, string> = {
  bug: "heroicons:bug-ant",
  feature: "heroicons:light-bulb",
  improvement: "heroicons:arrow-trending-up",
  question: "heroicons:question-mark-circle",
  other: "heroicons:chat-bubble-left-ellipsis",
};
