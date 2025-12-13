<script setup lang="ts">
import { useLessonController } from "~/composables/useLessonController";

definePageMeta({
  layout: "learning",
  middleware: ["auth", "enrolled-course"],
});

const route = useRoute();
const courseSlug = computed(() => route.params.course_slug as string);
const lessonSlug = computed(() => route.params.lesson_slug as string);

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
  markAsComplete,
  goToPreviousLesson,
  goToNextLesson,
  updateVideoProgress,
} = useLessonController({
  courseSlug: courseSlug.value,
  lessonSlug: lessonSlug.value,
});

// Adapted navigation for learning routes
const navigateToPrevious = () => {
  if (navigation.value?.previous) {
    navigateTo(
      `/learning/${courseSlug.value}/lessons/${navigation.value.previous.slug}`
    );
  }
};

const navigateToNext = () => {
  if (navigation.value?.next) {
    navigateTo(
      `/learning/${courseSlug.value}/lessons/${navigation.value.next.slug}`
    );
  }
};

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
  <div class="min-h-full">
    <!-- Loading State -->
    <div v-if="isLoading" class="p-6 lg:p-8 space-y-6">
      <USkeleton class="h-8 w-1/3 rounded-lg" />
      <USkeleton class="aspect-video w-full rounded-xl" />
      <USkeleton class="h-64 w-full rounded-xl" />
    </div>

    <!-- Content -->
    <template v-else-if="lesson">
      <!-- Lesson Header -->
      <div class="border-b border-default bg-elevated/50">
        <div class="px-6 py-4 flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2 text-sm text-muted">
              <span
                >Урок
                {{
                  navigation?.current_index !== undefined
                    ? navigation.current_index + 1
                    : ""
                }}</span
              >
              <span>из</span>
              <span>{{ navigation?.total_lessons }}</span>
            </div>
            <div class="h-4 w-px bg-default" />
            <h1 class="font-semibold text-default">{{ lesson.title }}</h1>
          </div>

          <!-- Completion Status -->
          <div class="flex items-center gap-3">
            <UBadge
              v-if="isCompleted"
              color="success"
              variant="subtle"
              icon="i-lucide-check-circle"
            >
              Завершён
            </UBadge>
            <UBadge
              v-else-if="progressPercent > 0"
              color="primary"
              variant="subtle"
            >
              {{ progressPercent }}% пройдено
            </UBadge>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="p-6 lg:p-8">
        <div class="max-w-4xl mx-auto space-y-6">
          <!-- Video Player -->
          <div
            v-if="hasVideo"
            class="rounded-xl overflow-hidden bg-black shadow-xl"
          >
            <LazyLessonsVideoPlayer
              :video-url="lesson.video_url!"
              :lesson-title="lesson.title"
              @progress="updateVideoProgress"
            />
          </div>

          <!-- Lesson Content (Markdown) -->
          <div class="bg-elevated rounded-xl border border-default p-6 lg:p-8">
            <div class="flex items-center gap-3 mb-6">
              <UIcon name="i-lucide-file-text" class="size-5 text-primary" />
              <h2 class="text-lg font-semibold text-default">Материал урока</h2>
              <div class="ml-auto flex items-center gap-2 text-sm text-muted">
                <UIcon name="i-lucide-clock" class="size-4" />
                <span>{{ lesson.duration_minutes }} мин</span>
              </div>
            </div>

            <LessonsContentViewer
              :title="lesson.title"
              :content="lesson.content"
              :duration="lesson.duration_minutes"
            />
          </div>

          <!-- Materials -->
          <div
            v-if="hasMaterials"
            class="bg-elevated rounded-xl border border-default overflow-hidden"
          >
            <div
              class="px-6 py-4 border-b border-default flex items-center gap-3"
            >
              <UIcon name="i-lucide-paperclip" class="size-5 text-primary" />
              <h2 class="text-lg font-semibold text-default">
                Материалы для скачивания
              </h2>
            </div>
            <LazyLessonsMaterialsList :materials="lesson.materials" />
          </div>

          <!-- Assignments Link -->
          <div
            v-if="hasAssignments"
            class="bg-warning/5 border border-warning/20 rounded-xl p-6 flex items-center justify-between"
          >
            <div class="flex items-center gap-4">
              <div
                class="size-12 rounded-full bg-warning/10 flex items-center justify-center"
              >
                <UIcon
                  name="i-lucide-clipboard-list"
                  class="size-6 text-warning"
                />
              </div>
              <div>
                <h3 class="font-semibold text-default">Задания к уроку</h3>
                <p class="text-sm text-muted">
                  {{ lesson.assignments_count }}
                  {{
                    lesson.assignments_count === 1 ? "задание" : "заданий"
                  }}
                  для выполнения
                </p>
              </div>
            </div>
            <UButton
              :to="`/learning/${courseSlug}/assignments?lesson=${lesson.slug}`"
              color="warning"
              variant="soft"
              trailing-icon="i-lucide-arrow-right"
            >
              Посмотреть
            </UButton>
          </div>

          <!-- Navigation Footer -->
          <div
            class="flex items-center justify-between pt-6 border-t border-default"
          >
            <!-- Previous -->
            <UButton
              v-if="canNavigatePrevious"
              color="neutral"
              variant="ghost"
              icon="i-lucide-arrow-left"
              @click="navigateToPrevious"
            >
              {{ navigation?.previous?.title }}
            </UButton>
            <div v-else />

            <!-- Complete Button -->
            <UButton
              v-if="!isCompleted"
              color="success"
              :loading="isCompletingLesson"
              icon="i-lucide-check"
              @click="markAsComplete"
            >
              Завершить урок
            </UButton>

            <!-- Next -->
            <UButton
              v-if="canNavigateNext"
              color="primary"
              trailing-icon="i-lucide-arrow-right"
              @click="navigateToNext"
            >
              {{ navigation?.next?.title }}
            </UButton>
            <div v-else />
          </div>
        </div>
      </div>
    </template>

    <!-- Error State -->
    <div v-else class="flex flex-col items-center justify-center py-20 gap-6">
      <UIcon name="i-lucide-file-x" class="size-16 text-muted" />
      <div class="text-center space-y-2">
        <h1 class="text-2xl font-bold text-default">Урок не найден</h1>
        <p class="text-muted">
          Возможно, урок был удалён или у вас нет к нему доступа
        </p>
      </div>
      <UButton
        :to="`/learning/${courseSlug}`"
        color="primary"
        icon="i-lucide-arrow-left"
      >
        Вернуться к курсу
      </UButton>
    </div>
  </div>
</template>
