<script setup lang="ts">
import { useLessonController } from "~/composables/useLessonController";

definePageMeta({
  layout: "default",
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
  allLessons,
  markAsComplete,
  updateVideoProgress,
} = useLessonController({
  courseSlug: courseSlug.value,
  lessonSlug: lessonSlug.value,
});

// Navigation helpers
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

// Breadcrumbs для header
const breadcrumbs = computed(() => [
  { label: "Обучение", to: "/learning", icon: "i-lucide-home" },
  {
    label: lesson.value?.course.title || "Курс",
    to: `/learning/${courseSlug.value}`,
  },
  { label: lesson.value?.title || "Урок" },
]);

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
    <LayoutContainer v-if="isLoading" class="py-8">
      <div class="space-y-2">
        <USkeleton class="h-8 w-1/3 rounded-lg" />
        <USkeleton class="aspect-video w-full rounded-xl" />
        <USkeleton class="h-64 w-full rounded-xl" />
      </div>
    </LayoutContainer>

    <!-- Content -->
    <template v-else-if="lesson">
      <!-- Compact Header Bar -->
      <div class="sticky top-0 z-40 border-b border-default">
        <LayoutContainer>
          <div class="py-3 flex items-center justify-between">
            <!-- Left: Breadcrumbs & Title -->
            <div class="flex items-center gap-2 min-w-0 flex-1">
              <UBreadcrumb :items="breadcrumbs" class="hidden sm:flex" />
              <div class="sm:hidden flex items-center gap-2 text-sm">
                <UButton
                  :to="`/learning/${courseSlug}`"
                  color="neutral"
                  variant="ghost"
                  icon="i-lucide-arrow-left"
                  size="xs"
                />
                <span class="text-muted truncate">{{
                  lesson.course.title
                }}</span>
              </div>
            </div>

            <!-- Right: Progress & Status -->
            <div class="flex items-center gap-2 shrink-0">
              <span class="text-sm text-muted hidden md:inline">
                Урок {{ (navigation?.current_index ?? 0) + 1 }} из
                {{ navigation?.total_lessons }}
              </span>
              <UBadge
                v-if="isCompleted"
                color="success"
                variant="subtle"
                icon="i-lucide-check-circle"
                size="sm"
              >
                Завершён
              </UBadge>
              <UBadge
                v-else-if="progressPercent > 0"
                color="primary"
                variant="subtle"
                size="sm"
              >
                {{ progressPercent }}%
              </UBadge>
            </div>
          </div>
        </LayoutContainer>
      </div>

      <!-- Main Layout: Content + Sidebar -->
      <LayoutContainer class="py-8">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-2">
          <!-- Main Content Area -->
          <div class="lg:col-span-8 space-y-2">
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
            <UCard>
              <template #header>
                <div class="flex items-center gap-2 mb-2">
                  <UIcon
                    name="i-lucide-file-text"
                    class="size-5 text-primary"
                  />
                  <h2 class="text-2xl font-bold text-default">
                    {{ lesson.title }}
                  </h2>
                  <div
                    class="ml-auto flex items-center gap-2 text-sm text-muted"
                  >
                    <UIcon name="i-lucide-clock" class="size-4" />
                    <span>{{ lesson.duration_minutes }} мин</span>
                  </div>
                </div>
              </template>

              <LessonsContentViewer
                :title="lesson.title"
                :content="lesson.content"
                :duration="lesson.duration_minutes"
              />
            </UCard>

            <!-- Materials -->
            <UCard v-if="hasMaterials" :ui="{ body: 'p-3' }">
              <div class="flex items-center gap-2 mb-2">
                <UIcon name="i-lucide-paperclip" class="size-5 text-primary" />
                <h2 class="text-xl font-bold text-default">
                  Материалы для скачивания
                </h2>
              </div>
              <LazyLessonsMaterialsList :materials="lesson.materials" />
            </UCard>

            <!-- Assignments Link -->
            <UCard
              v-if="hasAssignments"
              :ui="{ body: 'p-3' }"
              class="bg-warning/5 border-warning/20"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
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
                  size="lg"
                >
                  Посмотреть
                </UButton>
              </div>
            </UCard>

            <!-- Navigation Footer -->
            <div
              class="flex items-center justify-between pt-2 border-t border-default"
            >
              <!-- Previous -->
              <UButton
                v-if="canNavigatePrevious"
                color="neutral"
                variant="ghost"
                icon="i-lucide-arrow-left"
                size="lg"
                @click="navigateToPrevious"
              >
                <span class="hidden sm:inline">{{
                  navigation?.previous?.title
                }}</span>
                <span class="sm:hidden">Назад</span>
              </UButton>
              <div v-else />

              <!-- Complete Button -->
              <!-- TODO: implement on backend -->
              <!-- <UButton
                v-if="!isCompleted"
                color="success"
                :loading="isCompletingLesson"
                icon="i-lucide-check"
                size="lg"
                @click="markAsComplete"
              >
                Завершить урок
              </UButton> -->

              <!-- Next -->
              <UButton
                v-if="canNavigateNext"
                color="primary"
                trailing-icon="i-lucide-arrow-right"
                size="lg"
                @click="navigateToNext"
              >
                <span class="hidden sm:inline">{{
                  navigation?.next?.title
                }}</span>
                <span class="sm:hidden">Далее</span>
              </UButton>
              <div v-else />
            </div>
          </div>

          <!-- Sidebar -->
          <aside class="lg:col-span-4">
            <div class="sticky top-24 space-y-2">
              <!-- Course Progress Card -->
              <UCard>
                <div class="flex items-center gap-2 mb-2">
                  <NuxtImg
                    v-if="lesson.course.cover_image_url"
                    :src="lesson.course.cover_image_url"
                    class="size-10 rounded-lg object-cover"
                    :alt="lesson.course.title"
                  />
                  <div
                    v-else
                    class="size-10 rounded-lg bg-primary/10 flex items-center justify-center"
                  >
                    <UIcon
                      name="i-lucide-book-open"
                      class="size-6 text-primary"
                    />
                  </div>
                  <div class="min-w-0 flex-1">
                    <NuxtLink
                      :to="'/courses/' + lesson.course.slug"
                      class="font-semibold text-default text-xl truncate"
                    >
                      {{ lesson.course.title }}
                    </NuxtLink>
                    <p class="text-xs text-muted">
                      {{
                        navigation?.current_index !== undefined
                          ? navigation.current_index + 1
                          : 0
                      }}/{{ navigation?.total_lessons }} уроков
                    </p>
                  </div>
                </div>
                <UProgress
                  :model-value="
                    (((navigation?.current_index ?? 0) +
                      (isCompleted ? 1 : 0)) /
                      (navigation?.total_lessons || 1)) *
                    100
                  "
                  color="primary"
                  size="md"
                />
              </UCard>

              <!-- Lessons List -->
              <UCard>
                <template #header>
                  <h3 class="font-semibold text-2xl text-default">
                    Содержание курса
                  </h3>
                </template>
                <nav class="space-y-1 max-h-80 p-2 overflow-y-auto">
                  <UButton
                    v-for="(item, index) in allLessons"
                    :key="item.id"
                    :to="`/learning/${courseSlug}/lessons/${item.slug}`"
                    size="lg"
                    variant="outline"
                    :color="item.slug === lesson.slug ? 'primary' : 'neutral'"
                    :active="item.slug === lesson.slug"
                    class="w-full justify-start p-2 rounded-lg transition-colors"
                    :class="[
                      item.slug === lesson.slug
                        ? 'bg-primary/10 text-primary'
                        : 'hover:bg-muted/10 text-default',
                    ]"
                  >
                    <div
                      class="size-6 ring ring-default rounded-full flex items-center justify-center shrink-0 text-xs font-medium"
                      :class="[
                        item.slug === lesson.slug
                          ? 'bg-primary/20 text-primary'
                          : 'bg-muted/20 text-muted',
                      ]"
                    >
                      <span>{{ index + 1 }}</span>
                    </div>
                    <span class="text-lg truncate">{{ item.title }}</span>
                  </UButton>
                </nav>
              </UCard>
            </div>
          </aside>
        </div>
      </LayoutContainer>
    </template>

    <!-- Error State -->
    <LayoutContainer v-else class="py-20">
      <div class="flex flex-col items-center justify-center gap-2">
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
          size="lg"
        >
          Вернуться к курсу
        </UButton>
      </div>
    </LayoutContainer>
  </div>
</template>
