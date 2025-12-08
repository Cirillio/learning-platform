export interface Profile {
  user: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: "student" | "teacher";
  date_joined?: string;
  avatar?: string | null;
  bio?: string;
  phone?: string;
  birth_date: string | null;
  address?: string;
  city?: string;
  country?: string;
  specialization?: string;
  experience_years?: number | null;
  student_id?: string;
  enrollment_year?: number | null;
  created_at: string;
  updated_at: string;
}
