import { z } from "zod";
import {
  userSchema,
  rawUserProfileSchema,
  userRoleSchema,
} from "~/schemas/user.schema";

// ---------------------------------------------------------------------------
// Auth & Users
// ---------------------------------------------------------------------------

export type UserRole = z.infer<typeof userRoleSchema>;

export interface BasicUser {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
}

export type User = z.infer<typeof userSchema>;

// Для обратной совместимости, если где-то используется UserProfile как тип ответа бэкенда
export type UserProfile = z.infer<typeof rawUserProfileSchema>;
