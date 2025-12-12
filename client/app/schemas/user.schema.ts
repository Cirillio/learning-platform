import { z } from "zod";

export const userRoleSchema = z.enum(["student", "teacher", "admin"]);

// Базовая схема пользователя (как возвращает /auth/login/)
export const baseUserSchema = z.object({
  id: z.number(),
  username: z.string(),
  email: z.string().email(),
  first_name: z.string(),
  last_name: z.string(),
  role: userRoleSchema,
  date_joined: z.string(),
});

// Схема профиля с бэкенда (как возвращает /auth/profile/)
// Там поле user - это ID (number)
export const rawUserProfileSchema = z.object({
  user: z.number(),
  username: z.string(),
  email: z.string().email(),
  first_name: z.string(),
  last_name: z.string(),
  role: userRoleSchema,
  date_joined: z.string(),
  avatar: z.string().nullable().optional(),
  bio: z.string().optional(),
  phone: z.string().optional(),
  birth_date: z.string().nullable().optional(),
  address: z.string().optional(),
  city: z.string().optional(),
  country: z.string().optional(),
  specialization: z.string().optional(),
  experience_years: z.number().nullable().optional(),
  student_id: z.string().optional(),
  enrollment_year: z.number().nullable().optional(),
  created_at: z.string(),
  updated_at: z.string(),
});

// Единая схема пользователя для приложения (Internal)
// Объединяет базовые поля и поля профиля. ID всегда в поле `id`.
export const userSchema = baseUserSchema.extend({
  avatar: z.string().nullable().optional(),
  bio: z.string().optional(),
  phone: z.string().optional(),
  birth_date: z.string().nullable().optional(),
  address: z.string().optional(),
  city: z.string().optional(),
  country: z.string().optional(),
  specialization: z.string().optional(),
  experience_years: z.number().nullable().optional(),
  student_id: z.string().optional(),
  enrollment_year: z.number().nullable().optional(),
  created_at: z.string().optional(),
  updated_at: z.string().optional(),
});

export type User = z.infer<typeof userSchema>;
export type RawUserProfile = z.infer<typeof rawUserProfileSchema>;
