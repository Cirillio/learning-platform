// ~/types/index.ts

// Тип для профиля пользователя

// Тип для пользователя, который приходит с API
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: "student" | "teacher";
  date_joined: string;
  is_active?: boolean;
  avatar?: string | null;
  bio?: string;
}

// Тип для ответа от эндпоинта /auth/login/
export interface LoginResponse {
  user: User;
  access_token_exp: number;
  refresh_token_exp: number;
}

// Тип для категории курса
export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
  created_at: string;
}

// Базовый тип для курса (для списков)
export interface Course {
  id: number;
  title: string;
  slug: string;
  short_description: string;
  teacher: number; // ID преподавателя
  teacher_name: string;
  category: number; // ID категории
  category_name: string;
  cover_image: string | null;
  cover_image_url: string | null;
  status: "draft" | "published" | "archived";
  difficulty: "beginner" | "intermediate" | "advanced";
  duration_weeks: number | null;
  max_students: number | null;
  enrolled_count: number;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

// Расширенный тип для детальной страницы курса
// Используем Omit, чтобы избежать конфликта типов при наследовании
export type CourseDetail = Omit<Course, "teacher" | "category"> & {
  description: string;
  lessons_count: number;
  assignments_count: number;
  is_enrolled: boolean;
  progress: number;
  teacher: User; // В детальном виде преподаватель - это полный объект
  category: Category; // Категория - тоже полный объект
};

// Типы для фильтров курсов
export interface FilterOption {
  value: string;
  label: string;
}

export interface CourseFilterGroup {
  value: string;
  label: string;
  values: FilterOption[];
}

export interface CourseFiltersResponse {
  filters: CourseFilterGroup[];
}

// Типы для параметров запросов
export interface CourseFilters {
  category?: string;
  difficulty?: string;
  status?: string;
  search?: string;
  ordering?: string;
  page?: number;
  page_size?: number;
}

export interface CoursesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Course[];
}

export interface CategoriesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Category[];
}

// Типы для записи/отзаписи на курс
export interface CourseEnrollment {
  id: number;
  course_id: number;
  course_slug: string;
  enrolled_at: string;
  is_active: boolean;
  progress: number;
  unenrolled_at?: string; // Только для unenroll ответа
}

export interface CourseEnrollmentResponse {
  enrollments_count: number;
  spots_left: number | null;
}

export interface EnrollResponse {
  detail: string;
  enrollment: CourseEnrollment;
  course: CourseEnrollmentResponse;
}

export interface UnenrollResponse {
  detail: string;
  enrollment: Omit<CourseEnrollment, "enrolled_at"> & { unenrolled_at: string };
  course: CourseEnrollmentResponse;
}
