<script setup lang="ts">
import type { Course } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Мои курсы",
});

const api = useApi();
const authStore = useAuthStore();

interface CoursesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Course[];
}

const {
  data: coursesData,
  pending,
  refresh,
} = await useAsyncData<CoursesResponse>("teacher-all-courses", () =>
  api.get<CoursesResponse>("/courses/my_courses")
);

const courses = computed(() => coursesData.value?.results || []);

// Filters
const statusFilter = ref<string>("all");

const filteredCourses = computed(() => {
  if (statusFilter.value === "all") return courses.value;
  return courses.value.filter((c) => c.status === statusFilter.value);
});

// SEO
useHead({
  title: "Мои курсы | Преподаватель",
});
</script>

<template>
  <div>
    <!-- Header -->
    <TeacherCoursesHeader
      :status-filter="statusFilter"
      @update:status-filter="statusFilter = $event"
    />

    <!-- Loading -->
    <div
      v-if="pending"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <USkeleton v-for="i in 6" :key="i" class="h-64 rounded-xl" />
    </div>

    <!-- Empty State -->
    <TeacherCoursesEmptyState
      v-else-if="filteredCourses.length === 0"
      :status-filter="statusFilter"
      v-on:update="() => refresh()"
    />

    <!-- Courses Grid -->
    <TeacherCoursesGrid v-else :courses="filteredCourses" />
  </div>
</template>
