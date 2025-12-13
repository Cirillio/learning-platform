<script lang="ts" setup>
import type { Submission } from "~/types";

const formatDate = (date: string) => {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date));
};

interface Props {
  submission: Submission;
}

defineProps<Props>();
</script>

<template>
  <UButton
    :to="`/teacher/grading/${submission.id}`"
    variant="soft"
    color="neutral"
    class="flex items-center gap-4 p-3 transition-colors"
  >
    <UAvatar
      :alt="submission.student_name"
      size="2xl"
      class="bg-default text-base dark:*:text-white/75! ring-2 ring-muted"
    />
    <div class="flex-1 min-w-0">
      <p class="font-semibold text-xl text-default truncate">
        {{ submission.student_name }}
      </p>
      <p class="text-lg text-muted truncate">
        {{ submission.assignment_title }}
      </p>
    </div>
    <div class="text-right shrink-0">
      <UBadge v-if="submission.is_late" color="error" variant="soft" size="sm">
        Опоздание
      </UBadge>
      <p class="text-xs text-muted mt-1">
        {{ formatDate(submission.submitted_at) }}
      </p>
    </div>
  </UButton>
</template>
