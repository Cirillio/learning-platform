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
    class="min-h-screen bg-default pb-20 border-b border-default"
  >
    <!-- Header Section -->
    <CoursesDetailsHeader :course="course" :breadcrumbs="breadcrumbLinks" />

    <!-- Main Content & Sidebar Layout -->
    <LayoutContainer class="-mt-20 relative z-20">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-2">
        <!-- Left Column: Content -->
        <div class="lg:col-span-2 space-y-2">
          <!-- Description & Trusted By -->
          <CoursesDetailsDescription :description="course.description" />

          <!-- Course Guide (Syllabus) -->
          <CoursesDetailsSyllabus
            :lessons="lessons"
            :course-slug="slug"
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
          :pending="enrollPending"
          @enroll="handleEnroll"
          @unenroll="handleUnenroll"
        />
      </div>
    </LayoutContainer>
  </div>

  <!-- Loading State -->
  <div
    v-else-if="coursePending"
    class="min-h-screen flex items-center justify-center"
  >
    <UIcon name="i-lucide-loader-2" class="size-10 animate-spin text-primary" />
  </div>

  <!-- Error State -->
  <div
    v-else
    class="min-h-screen flex flex-col items-center justify-center gap-2"
  >
    <h1 class="text-2xl font-bold text-default">Курс не найден</h1>
    <UButton to="/courses" label="Вернуться в каталог" size="lg" />
  </div>
</template>
