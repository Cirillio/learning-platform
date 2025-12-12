import type { User, UserProfile } from "~/types";

export function normalizeUser(profile: UserProfile): User {
  return {
    id: profile.user,
    username: profile.username,
    email: profile.email,
    first_name: profile.first_name,
    last_name: profile.last_name,
    role: profile.role,
    date_joined: profile.date_joined,
    avatar: profile.avatar,
    bio: profile.bio,
    phone: profile.phone,
    birth_date: profile.birth_date,
    address: profile.address,
    city: profile.city,
    country: profile.country,
    specialization: profile.specialization,
    experience_years: profile.experience_years,
    student_id: profile.student_id,
    enrollment_year: profile.enrollment_year,
    created_at: profile.created_at,
    updated_at: profile.updated_at,
  };
}

export const getUserFromProfile = normalizeUser;
