import { z } from "zod";

// ---------------------------------------------------------------------------
// Lesson Material Schema
// ---------------------------------------------------------------------------

export const lessonMaterialSchema = z.object({
  id: z.number(),
  title: z.string(),
  file: z.string(),
  file_url: z.string(),
  file_type: z.string(),
  file_size: z.number(),
  description: z.string().optional(),
  order: z.number(),
  uploaded_at: z.string(),
});

// ---------------------------------------------------------------------------
// Lesson Schema
// ---------------------------------------------------------------------------

export const lessonSchema = z.object({
  id: z.number(),
  course: z.string(), // slug
  title: z.string(),
  slug: z.string(),
  description: z.string(),
  order: z.number(),
  duration_minutes: z.number(),
  is_published: z.boolean(),
  video_url: z.string().nullable().optional(),
  materials_count: z.number(),
  created_at: z.string(),
  updated_at: z.string(),
});

// ---------------------------------------------------------------------------
// Lesson Form Schemas
// ---------------------------------------------------------------------------

export const lessonCreateSchema = z.object({
  course: z.string().min(1, "Курс обязателен"),
  title: z
    .string()
    .min(3, "Минимум 3 символа")
    .max(200, "Максимум 200 символов"),
  slug: z.string().optional(),
  description: z.string().max(500, "Максимум 500 символов").optional(),
  content: z.string().optional(),
  order: z.number().min(1).optional(),
  duration_minutes: z.number().min(0).max(600).optional(),
  is_published: z.boolean().default(false),
  video_url: z
    .string()
    .url("Введите корректный URL")
    .optional()
    .or(z.literal("")),
});

export const lessonUpdateSchema = z.object({
  title: z
    .string()
    .min(3, "Минимум 3 символа")
    .max(200, "Максимум 200 символов")
    .optional(),
  slug: z.string().optional(),
  description: z.string().max(500, "Максимум 500 символов").optional(),
  content: z.string().optional(),
  order: z.number().min(1).optional(),
  duration_minutes: z.number().min(0).max(600).optional(),
  is_published: z.boolean().optional(),
  video_url: z
    .string()
    .url("Введите корректный URL")
    .optional()
    .or(z.literal("")),
});

// Form Schema для UForm
export const lessonFormSchema = z.object({
  title: z
    .string()
    .min(3, "Минимум 3 символа")
    .max(200, "Максимум 200 символов"),
  description: z.string().max(500, "Максимум 500 символов").optional(),
  content: z.string().optional(),
  video_url: z
    .string()
    .url("Введите корректный URL")
    .optional()
    .or(z.literal("")),
  duration_minutes: z.number().min(0, "Минимум 0").max(600, "Максимум 600"),
  is_published: z.boolean(),
});

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type LessonCreateInput = z.infer<typeof lessonCreateSchema>;
export type LessonUpdateInput = z.infer<typeof lessonUpdateSchema>;
export type LessonFormInput = z.infer<typeof lessonFormSchema>;
