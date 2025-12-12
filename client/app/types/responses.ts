import type { Course } from "./courses";
import type { Lesson } from "./lessons";
import type { Assignment } from "./assignments";
import type { Submission, Grade } from "./submissions";
import type { Notification } from "./notifications";
import type { Category } from "./courses";

// ---------------------------------------------------------------------------
// Generic Types
// ---------------------------------------------------------------------------

/**
 * Стандартный ответ пагинации DRF
 */
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

/**
 * Базовая структура для полей, которые есть почти везде
 */
export interface TimeStamped {
  created_at: string;
  updated_at: string;
}

// ---------------------------------------------------------------------------
// Courses
// ---------------------------------------------------------------------------

import type { CourseEnrollment } from "./courses";
import type { User } from "./user";

// Ответ при записи на курс
export interface EnrollmentResponse {
  detail: string;
  enrollment: CourseEnrollment;
  course: {
    enrollments_count: number;
    spots_left: number;
  };
}

export interface UnenrollResponse {
  detail: string;
  enrollment: Omit<CourseEnrollment, "enrolled_at"> & { unenrolled_at: string };
  course: {
    enrollments_count: number;
    spots_left: number;
  };
}

export interface UnreadCountResponse {
  count: number;
}

//
// Auth Responses
//

export interface AuthResponse {
  user: User;
}

export interface TokenRefreshResponse {
  access: string;
  refresh: string;
}

// ---------------------------------------------------------------------------
// Aliases for Services
// ---------------------------------------------------------------------------

// Основные ответы списков
export type CoursesResponse = PaginatedResponse<Course>;
export type LessonsResponse = PaginatedResponse<Lesson>;
export type AssignmentsResponse = PaginatedResponse<Assignment>;
export type SubmissionsResponse = PaginatedResponse<Submission>;
export type GradesResponse = PaginatedResponse<Grade>;
export type NotificationsResponse = PaginatedResponse<Notification>;
export type CategoriesResponse = PaginatedResponse<Category>;
