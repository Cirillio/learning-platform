<script setup lang="ts">
import type { CourseDetail, LessonWithProgress } from "~/types";
import { coursesService } from "~/services";

definePageMeta({
  layout: "default",
  middleware: ["auth", "enrolled-course"],
});

const route = useRoute();
const courseSlug = computed(() => route.params.course_slug as string);
const coursesApi = coursesService();

// Fetch course details
const { data: course, pending: coursePending } =
  await useAsyncData<CourseDetail>(`learning-course-${courseSlug.value}`, () =>
    coursesApi.getCourse(courseSlug.value)
  );

// Fetch lessons with progress
interface LessonsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: LessonWithProgress[];
}

const { data: lessonsResponse, pending: lessonsPending } =
  await useAsyncData<LessonsResponse>(
    `learning-lessons-${courseSlug.value}`,
    () => coursesApi.getCourseLessons(courseSlug.value)
  );

const lessons = computed(() => lessonsResponse.value?.results || []);

// Statistics
const completedLessons = computed(
  () => lessons.value.filter((l) => l.progress?.status === "completed").length
);

const totalLessons = computed(() => lessons.value.length);

const progressPercent = computed(() => {
  if (totalLessons.value === 0) return 0;
  return Math.round((completedLessons.value / totalLessons.value) * 100);
});

// Next lesson to continue
const nextLesson = computed(() => {
  const sorted = [...lessons.value].sort((a, b) => a.order - b.order);
  return sorted.find((l) => l.progress?.status !== "completed") || sorted[0];
});

// SEO
useHead(() => ({
  title: course.value ? `${course.value.title} | Обучение` : "Загрузка...",
}));
</script>

<template>
  <LayoutContainer class="py-8 bg-default space-y-2">
    <!-- Loading -->
    <div v-if="coursePending || lessonsPending" class="space-y-2">
      <USkeleton class="h-32 w-full rounded-xl" />
      <div class="grid grid-cols-1 md:grid-cols-3 gap-2">
        <USkeleton v-for="i in 3" :key="i" class="h-24 rounded-xl" />
      </div>
      <USkeleton class="h-96 w-full rounded-xl" />
    </div>

    <!-- Content -->
    <template v-else-if="course">
      <!-- Hero Card -->
      <LearningCourseHero
        :course="course"
        :course-slug="courseSlug"
        :next-lesson-slug="nextLesson?.slug"
        :completed-lessons="completedLessons"
      />

      <!-- Stats Cards -->
      <LearningStatsGrid
        :progress-percent="progressPercent"
        :completed-lessons="completedLessons"
        :total-lessons="totalLessons"
        :assignments-count="course.assignments_count || 0"
        :course-slug="courseSlug"
      />

      <!-- Lessons List -->
      <LearningLessonsList :lessons="lessons" :course-slug="courseSlug" />
    </template>

    <!-- Error State -->
    <div v-else class="flex flex-col items-center justify-center py-20 gap-2">
      <UIcon name="i-lucide-alert-circle" class="size-16 text-error" />
      <h2 class="text-2xl font-bold text-default">Курс не найден</h2>
      <UButton to="/learning" color="primary" size="lg">
        Вернуться в панель
      </UButton>
    </div>
  </LayoutContainer>
</template>
