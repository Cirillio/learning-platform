import { z } from "zod";

// ---------------------------------------------------------------------------
// Comment Validation Schemas
// ---------------------------------------------------------------------------

/**
 * Схема для создания комментария
 */
export const createCommentSchema = z.object({
  content_type: z.number().int().positive("Некорректный тип контента"),
  object_id: z.number().int().positive("Некорректный ID объекта"),
  text: z
    .string()
    .min(1, "Комментарий не может быть пустым")
    .max(1000, "Комментарий не должен превышать 1000 символов")
    .trim(),
  parent: z.number().int().positive().nullable().optional(),
});

/**
 * Схема для обновления комментария
 */
export const updateCommentSchema = z.object({
  text: z
    .string()
    .min(1, "Комментарий не может быть пустым")
    .max(1000, "Комментарий не должен превышать 1000 символов")
    .trim(),
});

/**
 * Схема для формы комментария (упрощенная, без content_type и object_id)
 */
export const commentFormSchema = z.object({
  text: z
    .string()
    .min(1, "Комментарий не может быть пустым")
    .max(1000, "Комментарий не должен превышать 1000 символов")
    .trim(),
});

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type CreateCommentInput = z.infer<typeof createCommentSchema>;
export type UpdateCommentInput = z.infer<typeof updateCommentSchema>;
export type CommentFormInput = z.infer<typeof commentFormSchema>;
