<script setup lang="ts">
import type { LessonWithProgress } from "~/types";

interface Props {
  lessons: LessonWithProgress[];
  courseSlug: string;
}

defineProps<Props>();
</script>

<template>
  <div class="bg-elevated rounded-xl border border-default overflow-hidden">
    <div class="px-6 py-4 border-b border-default">
      <h2 class="text-lg font-semibold text-default">Содержание курса</h2>
    </div>

    <div class="divide-y divide-default">
      <NuxtLink
        v-for="lesson in lessons"
        :key="lesson.id"
        :to="`/learning/${courseSlug}/lessons/${lesson.slug}`"
        class="flex items-center gap-4 px-6 py-4 hover:bg-muted/5 transition-colors group"
      >
        <!-- Order Number / Status Icon -->
        <div
          class="size-10 rounded-full flex items-center justify-center shrink-0 transition-colors"
          :class="[
            lesson.progress?.status === 'completed'
              ? 'bg-success/10 text-success'
              : lesson.progress?.status === 'in_progress'
              ? 'bg-primary/10 text-primary'
              : 'bg-muted/10 text-muted group-hover:bg-primary/10 group-hover:text-primary',
          ]"
        >
          <UIcon
            v-if="lesson.progress?.status === 'completed'"
            name="i-lucide-check"
            class="size-5"
          />
          <UIcon
            v-else-if="lesson.progress?.status === 'in_progress'"
            name="i-lucide-play"
            class="size-5"
          />
          <span v-else class="font-medium text-sm">{{ lesson.order }}</span>
        </div>

        <!-- Lesson Info -->
        <div class="flex-1 min-w-0">
          <h3
            class="font-medium text-default group-hover:text-primary transition-colors truncate"
          >
            {{ lesson.title }}
          </h3>
          <p class="text-sm text-muted truncate">
            {{ lesson.description }}
          </p>
        </div>

        <!-- Duration -->
        <div class="flex items-center gap-2 text-sm text-muted shrink-0">
          <UIcon name="i-lucide-clock" class="size-4" />
          <span>{{ lesson.duration_minutes }} мин</span>
        </div>

        <!-- Arrow -->
        <UIcon
          name="i-lucide-chevron-right"
          class="size-5 text-muted group-hover:text-primary transition-colors shrink-0"
        />
      </NuxtLink>
    </div>
  </div>
</template>
