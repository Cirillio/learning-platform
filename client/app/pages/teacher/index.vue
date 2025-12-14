<script setup lang="ts">
import type { User, CourseDetail } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["auth", "teacher-only"],
});

const toast = useToast();
const api = useApi();
const { user, logout } = useAuth();

// Fetch teacher's courses
interface CoursesResponse {
  count: number;
  results: CourseDetail[];
}

const {
  data: coursesData,
  pending: coursesPending,
  refresh: refreshCourses,
} = await useAsyncData<CoursesResponse>("teacher-courses", () =>
  api.get<CoursesResponse>("/courses/my_courses")
);

const courses = computed(() => coursesData.value?.results || []);

// Computed stats
const stats = computed(() => {
  const courseList = courses.value;
  return {
    totalCourses: courseList.length,
    publishedCourses: courseList.filter((c) => c.status === "published").length,
    totalStudents: courseList.reduce(
      (acc, c) => acc + (c.enrolled_count || 0),
      0
    ),
    totalLessons: courseList.reduce(
      (acc, c) => acc + (c.lessons_count || 0),
      0
    ),
  };
});

const handleLogout = async () => {
  try {
    await logout();
    navigateTo("/");
  } catch {
    toast.add({
      title: "Ошибка выхода",
      description: "Не удалось выйти из аккаунта",
      color: "error",
    });
  }
};

const fullName = computed(() => {
  return (
    `${user.value?.first_name || ""} ${user.value?.last_name || ""}`.trim() ||
    user.value?.username
  );
});

// SEO
useHead({
  title: "Профиль преподавателя",
});
</script>

<template>
  <div class="space-y-2">
    <!-- Header Card -->
    <TeacherProfileHeaderCard :user="user" @logout="handleLogout" />

    <!-- Quick Actions -->
    <TeacherProfileQuickActions />

    <div class="grid grid-cols-2 gap-2">
      <!-- My Courses -->
      <TeacherProfileCoursesCard
        :courses="courses"
        :pending="coursesPending"
        :refresh="refreshCourses"
      />
      <!-- Stats Grid -->
      <TeacherProfileStatsGrid :stats="stats" class="max-h-100" />
    </div>
  </div>
</template>
