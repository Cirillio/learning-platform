<script setup lang="ts">
import type { CourseDetail, Lesson } from "~/types";

const route = useRoute();
const slug = route.params.slug as string;

const { getCourse, getCourseLessons, enrollToCourse } = useCourses();
const { isAuthenticated } = useAuthStore();

// Fetch Course Details
const {
  data: course,
  pending: coursePending,
  error: courseError,
} = await getCourse(slug);

// Fetch Lessons (Syllabus)
const { data: lessonsResponse, pending: lessonsPending } =
  await getCourseLessons(slug);
const lessons = computed(
  () => (lessonsResponse.value as any)?.results || ([] as Lesson[])
);

// Computed properties for UI
const isUserEnrolled = computed(() => {
  if (!course.value) return false;
  return course.value.is_enrolled;
});

const breadcrumbLinks = computed(() => [
  { label: "Главная", to: "/" },
  { label: "Курсы", to: "/courses" },
  { label: course.value?.title || "Курс", to: `/courses/${slug}` },
]);

// Actions
const handleEnroll = async () => {
  if (!isAuthenticated) {
    navigateTo("/auth/login");
    return;
  }

  const result = await enrollToCourse(slug);
  if (result.success) {
    // Refresh data to update UI state
    refreshNuxtData(`course-${slug}`);
    // Show toast/notification (TODO)
  }
};
</script>

<template>
  <div
    v-if="course"
    class="min-h-screen bg-neutral-50 dark:bg-neutral-950 pb-20 border-b border-neutral-200 dark:border-neutral-800"
  >
    <!-- Header Section -->
    <CoursesDetailsHeader :course="course" :breadcrumbs="breadcrumbLinks" />

    <!-- Main Content & Sidebar Layout -->
    <UContainer class="-mt-16 relative z-20">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column: Content -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Description & Trusted By -->
          <CoursesDetailsDescription :description="course.description" />

          <!-- Course Guide (Syllabus) -->
          <CoursesDetailsSyllabus
            :lessons="lessons"
            :duration-weeks="course.duration_weeks"
          />

          <!-- Teacher Info -->
          <CoursesDetailsInstructor :teacher="course.teacher" />
        </div>

        <!-- Right Column: Sidebar (Sticky) -->
        <CoursesDetailsSidebar
          :course="course"
          :is-user-enrolled="isUserEnrolled"
          :lessons-count="lessons.length"
          @enroll="handleEnroll"
        />
      </div>
    </UContainer>
  </div>

  <!-- Loading State -->
  <div
    v-else-if="coursePending"
    class="min-h-screen flex items-center justify-center"
  >
    <UIcon
      name="i-heroicons-arrow-path"
      class="w-10 h-10 animate-spin text-primary-500"
    />
  </div>

  <!-- Error State -->
  <div
    v-else
    class="min-h-screen flex flex-col items-center justify-center gap-4"
  >
    <h1 class="text-2xl font-bold">Курс не найден</h1>
    <UButton to="/courses" label="Вернуться в каталог" />
  </div>
</template>

<style scoped>
/* Custom styles if needed, but mostly using Tailwind */
</style>
