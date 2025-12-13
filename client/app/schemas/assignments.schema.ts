import { z } from "zod";

// ---------------------------------------------------------------------------
// Assignment File Schema
// ---------------------------------------------------------------------------

export const assignmentFileSchema = z.object({
  id: z.number(),
  file: z.string(),
  file_url: z.string().url(),
  filename: z.string(),
  file_size: z.number(),
  uploaded_at: z.string().datetime(),
});

// ---------------------------------------------------------------------------
// Assignment Schema
// ---------------------------------------------------------------------------

export const assignmentSchema = z.object({
  id: z.number(),
  lesson: z.string(), // slug
  title: z.string().min(1, "Название обязательно"),
  description: z.string(),
  instructions: z.string(),
  max_score: z.number().min(0).max(1000),
  due_date: z.string().datetime().nullable().optional(),
  is_required: z.boolean(),
  allow_late_submission: z.boolean(),
  files: z.array(assignmentFileSchema),
  submissions_count: z.number(),
  is_submitted: z.boolean().optional(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

// ---------------------------------------------------------------------------
// Submission Schema
// ---------------------------------------------------------------------------

export const submissionStatusSchema = z.enum(["pending", "graded", "returned"]);

export const submissionFileSchema = z.object({
  id: z.number(),
  file: z.string(),
  file_url: z.string().url(),
  filename: z.string(),
  file_size: z.number(),
  uploaded_at: z.string().datetime(),
});

export const submissionSchema = z.object({
  id: z.number(),
  assignment: z.number(),
  assignment_title: z.string(),
  student: z.number(),
  student_name: z.string(),
  content: z.string(),
  status: submissionStatusSchema,
  is_late: z.boolean(),
  files_count: z.number(),
  submitted_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export const submissionDetailSchema = submissionSchema.extend({
  files: z.array(submissionFileSchema),
});

// ---------------------------------------------------------------------------
// Grade Schema
// ---------------------------------------------------------------------------

export const gradeSchema = z.object({
  id: z.number(),
  submission: z.number(),
  submission_content: z.string(),
  student_name: z.string(),
  assignment_title: z.string(),
  score: z.number().min(0),
  feedback: z.string().optional(),
  graded_by: z.number(),
  graded_by_name: z.string(),
  graded_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

// ---------------------------------------------------------------------------
// Form Schemas (for validation)
// ---------------------------------------------------------------------------

export const createSubmissionSchema = z.object({
  assignment: z.number(),
  content: z
    .string()
    .min(1, "Ответ обязателен")
    .max(10000, "Слишком длинный ответ"),
});

export const updateSubmissionSchema = z.object({
  content: z
    .string()
    .min(1, "Ответ обязателен")
    .max(10000, "Слишком длинный ответ")
    .optional(),
});

export const gradeSubmissionSchema = z.object({
  score: z.number().min(0, "Оценка не может быть отрицательной"),
  feedback: z.string().max(5000, "Комментарий слишком длинный").optional(),
});

// ---------------------------------------------------------------------------
// Type exports
// ---------------------------------------------------------------------------

export type AssignmentFileInput = z.infer<typeof assignmentFileSchema>;
export type AssignmentInput = z.infer<typeof assignmentSchema>;
export type SubmissionInput = z.infer<typeof submissionSchema>;
export type SubmissionDetailInput = z.infer<typeof submissionDetailSchema>;
export type GradeInput = z.infer<typeof gradeSchema>;
export type CreateSubmissionInput = z.infer<typeof createSubmissionSchema>;
export type UpdateSubmissionInput = z.infer<typeof updateSubmissionSchema>;
export type GradeSubmissionInput = z.infer<typeof gradeSubmissionSchema>;
