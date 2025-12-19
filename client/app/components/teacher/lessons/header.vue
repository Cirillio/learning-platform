<script setup lang="ts">
import type { LessonDetail } from "~/types";

defineProps<{
  lesson: LessonDetail;
  courseSlug: string;
  assignmentsCount: number;
}>();

const emit = defineEmits<{
  (e: "delete"): void;
}>();
</script>

<template>
  <div class="flex items-start justify-between gap-4">
    <div class="flex-1">
      <div class="flex items-center gap-3 mb-2">
        <UBadge color="primary" variant="soft" size="lg">
          Урок {{ lesson.order }}
        </UBadge>
        <UBadge
          v-if="!lesson.is_published"
          color="warning"
          variant="soft"
          size="lg"
        >
          Черновик
        </UBadge>
        <UBadge v-else color="success" variant="soft" size="lg">
          Опубликован
        </UBadge>
      </div>
      <h1 class="text-3xl font-bold text-default mb-2">
        {{ lesson.title }}
      </h1>
      <p class="text-lg text-muted">
        {{ lesson.description }}
      </p>
      <div class="flex items-center gap-4 mt-3 text-sm text-muted">
        <span class="flex items-center gap-1">
          <UIcon name="i-lucide-clock" class="size-4" />
          {{ lesson.duration_minutes }} мин
        </span>
        <span class="flex items-center gap-1">
          <UIcon name="i-lucide-paperclip" class="size-4" />
          {{ lesson.materials?.length || 0 }} материалов
        </span>
        <span class="flex items-center gap-1">
          <UIcon name="i-lucide-clipboard-list" class="size-4" />
          {{ assignmentsCount }} заданий
        </span>
      </div>
    </div>
    <div class="flex gap-2 shrink-0">
      <UButton
        color="neutral"
        variant="ghost"
        icon="i-lucide-arrow-left"
        :to="`/teacher/courses/${courseSlug}/lessons`"
      >
        Назад
      </UButton>
      <UButton
        color="primary"
        icon="i-lucide-pencil"
        :to="`/teacher/courses/${courseSlug}/lessons/${lesson.slug}/edit`"
      >
        Редактировать
      </UButton>
      <UButton
        color="error"
        variant="ghost"
        icon="i-lucide-trash-2"
        @click="emit('delete')"
      />
    </div>
  </div>
</template>
