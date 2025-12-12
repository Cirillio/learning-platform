import type { BasicUser } from "./user";

// ---------------------------------------------------------------------------
// Categories
// ---------------------------------------------------------------------------

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  icon?: string;
  created_at: string;
}

export type CourseStatus = "draft" | "published" | "archived";
export type CourseDifficulty = "beginner" | "intermediate" | "advanced";

// Базовая модель курса (используется в списках)
export interface Course {
  id: number;
  title: string;
  slug: string;
  abbr: string;
  short_description: string;
  // В списке приходят ID и имена, чтобы не тянуть вложенные объекты
  teacher: number;
  teacher_name: string;
  category: number;
  category_name: string;
  cover_image: string | null;
  cover_image_url?: string | null;
  status: CourseStatus;
  difficulty: CourseDifficulty;
  duration_weeks: number | null;
  max_students: number | null;
  enrolled_count: number;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

// Детальная модель курса (расширенная)
export interface CourseDetail extends Omit<Course, "teacher" | "category"> {
  description: string;
  teacher: BasicUser; // Полный объект автора (BasicUserSerializer)
  category: Category; // Полный объект категории
  lessons_count: number;
  assignments_count: number;
  // Поля, доступные только авторизованным
  is_enrolled?: boolean;
  progress?: number;
}

// Студент в списке участников курса (для учителя)
export interface CourseStudent {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  enrolled_at: string;
  progress: number;
}

export interface CourseEnrollment {
  id: number;
  course_id: number;
  course_slug: string;
  enrolled_at: string;
  is_active: boolean;
  progress: number;
  unenrolled_at?: string;
}
