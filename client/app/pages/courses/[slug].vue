<script setup lang="ts">
import { useCoursesService } from "~/services";
import type { CourseDetail, Lesson } from "~/types";

const route = useRoute();
const toast = useToast();
const slug = route.params.slug as string;

const { isAuthenticated } = useAuthStore();
const coursesService = useCoursesService();
const { enrollToCourse, unenrollFromCourse } = coursesService;

const courseCacheKey = computed(() => `course-${slug}`);
const lessongsCacheKey = computed(() => `course-${slug}-lessons`);

const enrollPending = ref(false);

// Fetch Course Details
const {
  data: course,
  pending: coursePending,
  error: courseError,
} = await useAsyncData<CourseDetail>(courseCacheKey.value, () =>
  coursesService.getCourse(slug)
);

// Fetch Lessons (Syllabus)
const { data: lessonsResponse, pending: lessonsPending } = await useAsyncData(
  lessongsCacheKey.value,
  () => coursesService.getCourseLessons(slug)
);
const lessons = computed(
  () => (lessonsResponse.value as any)?.results || ([] as Lesson[])
);

// Computed properties for UI
const isUserEnrolled = computed<boolean>(() => {
  if (!course.value) return false;
  return course.value.is_enrolled || false;
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

  enrollPending.value = true;

  try {
    await enrollToCourse(slug);
    // Refresh data to update UI state
    refreshNuxtData(`course-${slug}`);
    toast.add({
      title: "Вы успешно записались на курс!",
      color: "success",
    });
    // Show toast/notification (TODO)
  } catch (e) {
    console.error(e);
  }
  enrollPending.value = false;
};

const handleUnenroll = async () => {
  if (!isAuthenticated) {
    navigateTo("/auth/login");
    return;
  }

  enrollPending.value = true;

  try {
    await unenrollFromCourse(slug);
    // Refresh data to update UI state
    refreshNuxtData(`course-${slug}`);
    // Show toast/notification (TODO)
    toast.add({
      title: "Вы успешно отписались от курса.",
      color: "info",
    });
  } catch (e) {
    console.error(e);
  }
  enrollPending.value = false;
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
          @unenroll="handleUnenroll"
          :pending="enrollPending"
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
