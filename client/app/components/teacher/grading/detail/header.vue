<script setup lang="ts">
import type { SubmissionDetail } from "~/types";

defineProps<{
  submission: SubmissionDetail;
  isGraded: boolean;
}>();

const formatDate = (date: string) => {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date));
};
</script>

<template>
  <div class="mb-8">
    <NuxtLink
      to="/teacher/grading"
      class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors mb-4"
    >
      <UIcon name="i-lucide-arrow-left" class="size-4" />
      Назад к списку
    </NuxtLink>

    <div class="flex items-start justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-default mb-2">
          {{ submission.assignment_title }}
        </h1>
        <div class="flex items-center gap-4 text-muted">
          <span class="flex items-center gap-2">
            <UAvatar :alt="submission.student_name" size="xs" />
            {{ submission.student_name }}
          </span>
          <span>{{ formatDate(submission.submitted_at) }}</span>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <UBadge :color="isGraded ? 'success' : 'warning'" size="lg">
          {{ isGraded ? "Оценено" : "На проверке" }}
        </UBadge>
        <UBadge v-if="submission.is_late" color="error" size="lg">
          Опоздание
        </UBadge>
      </div>
    </div>
  </div>
</template>
