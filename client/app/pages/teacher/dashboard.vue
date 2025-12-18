<script setup lang="ts">
import { page } from "#build/ui";
import type { Course, PaginatedResponse, Submission } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Панель управления",
});

const api = useApi();
const authStore = useAuthStore();

// Fetch teacher's courses
interface CoursesResponse {
  count: number;
  results: Course[];
}

const { data: coursesData, pending: coursesPending } = await useAsyncData<
  PaginatedResponse<Course>
>("teacher-courses", () =>
  api.get<PaginatedResponse<Course>>("/courses/", {
    page_size: 999,
  })
);

const courses = computed(() => coursesData.value?.results || []);

// Fetch pending submissions (ungraded)
interface SubmissionsResponse {
  count: number;
  results: Submission[];
}

const {
  data: submissionsData,
  pending: submissionsPending,
  refresh: refreshSubmissions,
} = await useAsyncData<SubmissionsResponse>("teacher-pending-submissions", () =>
  api.get<SubmissionsResponse>("/submissions/", {
    status: "pending",
  })
);

const pendingSubmissions = computed(() => submissionsData.value?.results || []);

// Stats
const totalStudents = computed(() => {
  return courses.value.reduce(
    (acc, course) => acc + (course.enrolled_count || 0),
    0
  );
});

const totalCourses = computed(() => courses.value.length);
const pendingCount = computed(() => submissionsData.value?.count || 0);
const publishedCount = computed(
  () => courses.value.filter((c) => c.status === "published").length
);

// Stats items for the grid
const statsItems = computed(() => [
  {
    label: "Курсы",
    value: totalCourses.value,
    icon: "i-lucide-book-open",
    iconColor: "text-primary",
    bgColor: "bg-primary/10",
    link: { to: "/teacher/courses", text: "Управлять →" },
  },
  {
    label: "Студенты",
    value: totalStudents.value,
    icon: "i-lucide-users",
    iconColor: "text-success",
    bgColor: "bg-success/10",
    subtitle: "Всего записано",
  },
  {
    label: "На проверке",
    value: pendingCount.value,
    icon: "i-lucide-clock",
    iconColor: "text-warning",
    bgColor: "bg-warning/10",
    link:
      pendingCount.value > 0
        ? { to: "/teacher/grading", text: "Проверить →" }
        : undefined,
    subtitle: pendingCount.value === 0 ? "Всё проверено" : undefined,
  },
  {
    label: "Опубликовано",
    value: publishedCount.value,
    icon: "i-lucide-globe",
    iconColor: "text-info",
    bgColor: "bg-info/10",
    subtitle: "Публичных курсов",
  },
]);

// Recent submissions (last 5)
const recentSubmissions = computed(() => pendingSubmissions.value.slice(0, 5));

// SEO
useHead({
  title: "Панель преподавателя",
});
</script>

<template>
  <div class="space-y-2">
    <!-- Welcome Section -->
    <TeacherDashboardWelcomeHero
      :user-name="authStore.user?.first_name || authStore.user?.username || ''"
    />

    <!-- Stats Grid -->
    <TeacherDashboardStatsCards :stats="statsItems" />

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-2">
      <!-- Recent Submissions -->
      <div class="lg:col-span-2">
        <TeacherSubmissionsItemList
          :submissions="recentSubmissions"
          :pending="submissionsPending"
          v-on:update="() => refreshSubmissions()"
        />
      </div>

      <!-- Courses List -->
      <TeacherCoursesMyListSidebar
        :courses="courses"
        :pending="coursesPending"
      />
    </div>
  </div>
</template>
