/**
 * Type definitions for the application
 * Following TypeScript best practices from instructions
 */

// User types
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: "teacher" | "student";
  is_active: boolean;
  date_joined: string;
  profile?: UserProfile;
}

export interface UserProfile {
  avatar?: string;
  bio?: string;
  phone?: string;
  address?: string;
}

// Auth types
export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  user: User;
  tokens: AuthTokens;
}

// API types
export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
  status?: number;
}

export interface ApiResponse<T = unknown> {
  data?: T;
  error?: ApiError;
  message?: string;
}

// Utility types
export type Role = "teacher" | "student";

export type UserRole = User["role"];
