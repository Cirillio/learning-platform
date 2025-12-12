<script setup lang="ts">
import { useLessonController } from "~/composables/useLessonController";

definePageMeta({
  middleware: ["auth"],
  layout: "default",
});

const route = useRoute();
const courseSlug = computed(() => route.params.slug as string);
const lessonSlug = computed(() => route.params.lessonSlug as string);

// Controller для управления состоянием урока
const {
  lesson,
  navigation,
  isLoading,
  isCompleted,
  isCompletingLesson,
  progressPercent,
  hasVideo,
  hasMaterials,
  hasAssignments,
  canNavigatePrevious,
  canNavigateNext,
  breadcrumbs,
  allLessons,
  markAsComplete,
  goToPreviousLesson,
  goToNextLesson,
  updateVideoProgress,
} = useLessonController({
  courseSlug: courseSlug.value,
  lessonSlug: lessonSlug.value,
});

// SEO
useHead(() => ({
  title: lesson.value?.title
    ? `${lesson.value.title} | ${lesson.value.course.title}`
    : "Загрузка урока...",
  meta: [
    {
      name: "description",
      content: lesson.value?.description || "Просмотр урока курса",
    },
  ],
}));
</script>

<template>
  <div class="min-h-screen bg-default">
    <!-- Loading State -->
    <SkeletonsLessonPage v-if="isLoading" />

    <!-- Content -->
    <template v-else-if="lesson">
      <!-- Header с хлебными крошками и прогрессом -->
      <LessonsHeader
        :lesson="lesson"
        :breadcrumbs="breadcrumbs"
        :progress-percent="progressPercent"
        :is-completed="isCompleted"
      />

      <!-- Main Layout: Content + Sidebar -->
      <LayoutContainer class="py-8">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-2">
          <!-- Main Content Area -->
          <div class="lg:col-span-8 space-y-2">
            <!-- Video Player (lazy loaded) -->
            <LazyLessonsVideoPlayer
              v-if="hasVideo"
              :video-url="lesson.video_url!"
              :lesson-title="lesson.title"
              @progress="updateVideoProgress"
            />

            <!-- Lesson Content (Markdown) -->
            <LessonsContentViewer
              :title="lesson.title"
              :content="lesson.content"
              :duration="lesson.duration_minutes"
            />

            <!-- Materials Section -->
            <LazyLessonsMaterialsList
              v-if="hasMaterials"
              :materials="lesson.materials"
            />

            <!-- Navigation Footer -->
            <LessonsNavFooter
              :navigation="navigation"
              :is-completed="isCompleted"
              :is-completing="isCompletingLesson"
              @previous="goToPreviousLesson"
              @next="goToNextLesson"
              @complete="markAsComplete"
            />
          </div>

          <!-- Sidebar -->
          <aside class="lg:col-span-4">
            <div class="sticky top-24 space-y-2">
              <!-- Course Progress Card -->
              <LessonsSidebarProgress
                :course="lesson.course"
                :navigation="navigation"
                :is-completed="isCompleted"
              />

              <!-- Lessons List -->
              <LessonsSidebarList
                :lessons="allLessons"
                :current-lesson-slug="lesson.slug"
                :course-slug="courseSlug"
              />

              <!-- Assignments Preview -->
              <LessonsSidebarAssignments
                v-if="hasAssignments"
                :lesson-slug="lesson.slug"
                :assignments-count="lesson.assignments_count"
              />
            </div>
          </aside>
        </div>
      </LayoutContainer>
    </template>

    <!-- Error State -->
    <div
      v-else
      class="min-h-screen flex flex-col items-center justify-center gap-6"
    >
      <UIcon name="i-lucide-file-x" class="size-16 text-muted" />
      <div class="text-center space-y-2">
        <h1 class="text-2xl font-bold text-default">Урок не найден</h1>
        <p class="text-muted">
          Возможно, урок был удалён или у вас нет к нему доступа
        </p>
      </div>
      <UButton
        :to="`/courses/${courseSlug}`"
        label="Вернуться к курсу"
        color="primary"
        variant="solid"
        icon="i-lucide-arrow-left"
      />
    </div>
  </div>
</template>
