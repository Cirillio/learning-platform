import { z } from "zod";

// Login schema
export const loginSchema = z.object({
  username: z
    .string()
    .min(1, "Имя пользователя обязательно")
    .min(3, "Имя пользователя должно содержать минимум 3 символа")
    .max(150, "Имя пользователя не должно превышать 150 символов"),

  password: z
    .string()
    .min(1, "Пароль обязателен")
    .min(8, "Пароль должен содержать минимум 8 символов"),

  remember: z.boolean().optional().default(false),
});

// Register schema
export const registerSchema = z
  .object({
    username: z
      .string()
      .min(1, "Имя пользователя обязательно")
      .min(3, "Имя пользователя должно содержать минимум 3 символа")
      .max(150, "Имя пользователя не должно превышать 150 символов")
      .regex(
        /^[a-zA-Z0-9_]+$/,
        "Имя пользователя может содержать только буквы, цифры и подчеркивания"
      ),

    email: z.string().min(1, "Email обязателен").email("Неверный формат email"),

    password: z
      .string()
      .min(1, "Пароль обязателен")
      .min(8, "Пароль должен содержать минимум 8 символов")
      .regex(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
        "Пароль должен содержать минимум одну заглавную букву, одну строчную букву и одну цифру"
      ),

    password_confirm: z.string().min(1, "Подтверждение пароля обязательно"),

    first_name: z
      .string()
      .min(1, "Имя обязательно")
      .max(30, "Имя не должно превышать 30 символов"),

    last_name: z
      .string()
      .min(1, "Фамилия обязательна")
      .max(30, "Фамилия не должна превышать 30 символов"),

    role: z.enum(["teacher", "student"], {
      message: "Выберите роль: преподаватель или студент",
    }),
  })
  .refine((data) => data.password === data.password_confirm, {
    message: "Пароли не совпадают",
    path: ["password_confirm"],
  });

// Profile update schema
export const profileUpdateSchema = z.object({
  first_name: z
    .string()
    .min(1, "Имя обязательно")
    .max(30, "Имя не должно превышать 30 символов"),

  last_name: z
    .string()
    .min(1, "Фамилия обязательна")
    .max(30, "Фамилия не должна превышать 30 символов"),

  email: z.string().min(1, "Email обязателен").email("Неверный формат email"),
});

// Password change schema
export const passwordChangeSchema = z
  .object({
    old_password: z.string().min(1, "Текущий пароль обязателен"),

    new_password: z
      .string()
      .min(1, "Новый пароль обязателен")
      .min(8, "Пароль должен содержать минимум 8 символов")
      .regex(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
        "Пароль должен содержать минимум одну заглавную букву, одну строчную букву и одну цифру"
      ),

    new_password_confirm: z
      .string()
      .min(1, "Подтверждение нового пароля обязательно"),
  })
  .refine((data) => data.new_password === data.new_password_confirm, {
    message: "Пароли не совпадают",
    path: ["new_password_confirm"],
  });

// Type exports
export type LoginForm = z.infer<typeof loginSchema>;
export type RegisterForm = z.infer<typeof registerSchema>;
export type ProfileUpdateForm = z.infer<typeof profileUpdateSchema>;
export type PasswordChangeForm = z.infer<typeof passwordChangeSchema>;
