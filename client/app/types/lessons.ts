import type { Course } from "./courses";

// ---------------------------------------------------------------------------
// Lessons
// ---------------------------------------------------------------------------

export interface LessonMaterial {
  id: number;
  title: string;
  file: string; // url
  file_url: string;
  file_type: string;
  file_size: number;
  description?: string;
  order: number;
  uploaded_at: string;
}

// Урок в списке
export interface Lesson {
  id: number;
  course: string; // slug
  title: string;
  slug: string;
  description: string;
  order: number;
  duration_minutes: number;
  is_published: boolean;
  video_url?: string | null;
  materials_count: number;
  created_at: string;
  updated_at: string;
}

// Детали урока
export interface LessonDetail extends Omit<Lesson, "course"> {
  course: Course; // Объект курса (CourseSerializer)
  content: string; // Markdown текст
  materials: LessonMaterial[];
  assignments_count: number;
}

// ---------------------------------------------------------------------------
// Lesson Progress & Navigation
// ---------------------------------------------------------------------------

export type LessonCompletionStatus =
  | "not_started"
  | "in_progress"
  | "completed";

export interface LessonProgress {
  lesson_id: number;
  status: LessonCompletionStatus;
  completed_at?: string | null;
  progress_percent: number;
}

export interface LessonNavigation {
  previous: Pick<Lesson, "id" | "slug" | "title" | "order"> | null;
  next: Pick<Lesson, "id" | "slug" | "title" | "order"> | null;
  current_index: number;
  total_lessons: number;
}

export interface LessonWithProgress extends Lesson {
  progress?: LessonProgress;
  is_accessible: boolean;
}

// Полный ответ для страницы урока
export interface LessonViewData {
  lesson: LessonDetail;
  navigation: LessonNavigation;
  progress?: LessonProgress;
  is_enrolled: boolean;
}

// Ответ на завершение урока
export interface MarkLessonCompleteResponse {
  success: boolean;
  message: string;
  progress: LessonProgress;
}
