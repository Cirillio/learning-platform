<script setup lang="ts">
import type { LessonDetail } from "~/types";

defineProps<{
  lesson: LessonDetail;
  courseSlug: string;
}>();
</script>

<template>
  <UCard class="bg-primary/5 border-primary/20">
    <div class="flex items-center gap-4">
      <div class="p-3 bg-primary/10 rounded-lg">
        <UIcon name="i-lucide-book-open" class="size-6 text-primary" />
      </div>
      <div class="flex-1">
        <div class="text-sm text-muted mb-1">Урок</div>
        <NuxtLink
          :to="`/teacher/courses/${courseSlug}/lessons/${lesson.slug}`"
          class="text-lg font-semibold text-default hover:text-primary transition-colors"
        >
          {{ lesson.order }}. {{ lesson.title }}
        </NuxtLink>
        <p
          v-if="lesson.description"
          class="text-sm text-muted mt-1 line-clamp-2"
        >
          {{ lesson.description }}
        </p>
      </div>
      <UButton
        :to="`/teacher/courses/${courseSlug}/lessons/${lesson.slug}`"
        color="primary"
        variant="soft"
        icon="i-lucide-external-link"
        size="sm"
      >
        Перейти к уроку
      </UButton>
    </div>
  </UCard>
</template>
