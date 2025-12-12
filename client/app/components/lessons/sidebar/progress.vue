<script setup lang="ts">
import type { Course, LessonNavigation } from "~/types";

interface Props {
  course: Course;
  navigation: LessonNavigation | null;
  isCompleted: boolean;
}

const props = defineProps<Props>();

// Прогресс курса (в %)
const courseProgress = computed(() => {
  if (!props.navigation) return 0;
  // Простая формула: (текущий урок / всего уроков) * 100
  // В реальном приложении это должно приходить с бэкенда
  const completedLessons = props.isCompleted
    ? props.navigation.current_index + 1
    : props.navigation.current_index;
  return Math.round((completedLessons / props.navigation.total_lessons) * 100);
});
</script>

<template>
  <UCard class="dark:bg-muted/25 bg-muted/75">
    <!-- Course Info -->
    <div class="p-4 border-b border-default">
      <div class="flex items-start gap-3">
        <img
          v-if="course.cover_image_url"
          :src="course.cover_image_url"
          :alt="course.title"
          class="size-12 rounded-lg object-cover"
        />
        <div
          v-else
          class="size-12 rounded-lg bg-primary/10 flex items-center justify-center"
        >
          <UIcon name="i-lucide-graduation-cap" class="size-6 text-primary" />
        </div>

        <div class="flex-1 min-w-0">
          <NuxtLink
            :to="`/courses/${course.slug}`"
            class="font-medium text-default hover:text-primary transition-colors line-clamp-2"
          >
            {{ course.title }}
          </NuxtLink>
          <p class="text-sm text-muted mt-0.5">
            {{ course.teacher_name }}
          </p>
        </div>
      </div>
    </div>

    <!-- Progress -->
    <div class="p-4 space-y-3">
      <div class="flex items-center justify-between text-sm">
        <span class="text-muted">Прогресс курса</span>
        <span class="font-medium text-default">{{ courseProgress }}%</span>
      </div>

      <!-- Progress Bar -->
      <div class="relative h-2 bg-muted rounded-full overflow-hidden">
        <div
          class="absolute inset-y-0 left-0 bg-primary rounded-full transition-all duration-500"
          :style="{ width: `${courseProgress}%` }"
        />
      </div>

      <!-- Stats -->
      <div v-if="navigation" class="grid grid-cols-2 gap-4 pt-2">
        <div class="text-center p-3 bg-muted/30 rounded-lg">
          <p class="text-lg font-semibold text-default">
            {{ navigation.current_index + 1 }}
          </p>
          <p class="text-xs text-muted">Текущий урок</p>
        </div>
        <div class="text-center p-3 bg-muted/30 rounded-lg">
          <p class="text-lg font-semibold text-default">
            {{ navigation.total_lessons }}
          </p>
          <p class="text-xs text-muted">Всего уроков</p>
        </div>
      </div>
    </div>
  </UCard>
</template>
