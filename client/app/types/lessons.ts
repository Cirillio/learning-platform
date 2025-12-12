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
