<script lang="ts" setup>
import type { Submission } from "~/types";

interface Props {
  submission: Submission;
}

defineProps<Props>();

const formatDate = (date: string) => {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date));
};
</script>

<template>
  <tr class="dark:hover:bg-muted/50 hover:bg-default/75 transition-colors">
    <!-- Student -->
    <td class="px-6 py-4">
      <div class="flex items-center gap-3">
        <NuxtLink
          :to="'/teacher/students/' + submission.student"
          class="font-semibold text-xl border-b-2 border-transparent hover:border-muted focus:border-muted active:border-muted transition-all text-default"
          >{{ submission.student_name }}</NuxtLink
        >
      </div>
    </td>

    <!-- Assignment -->
    <td class="px-6 py-4">
      <span class="text-default">{{ submission.assignment_title }}</span>
    </td>

    <!-- Status -->
    <td class="px-6 py-4">
      <UBadge
        size="lg"
        :color="
          submission.status === 'graded'
            ? 'success'
            : submission.status === 'pending'
            ? 'warning'
            : 'info'
        "
        variant="soft"
        class="w-full justify-center"
      >
        {{
          submission.status === "graded"
            ? "Оценено"
            : submission.status === "pending"
            ? "На проверке"
            : "Возвращено"
        }}
      </UBadge>
      <UBadge
        v-if="submission.is_late"
        color="error"
        variant="soft"
        size="lg"
        class="w-full justify-center"
      >
        Опоздание
      </UBadge>
    </td>

    <!-- Date -->
    <td class="px-6 py-4 text-lg text-muted">
      {{ formatDate(submission.submitted_at) }}
    </td>

    <!-- Actions -->
    <td class="px-6 py-4 text-right">
      <UButton
        :to="`/teacher/grading/${submission.id}`"
        :color="submission.status === 'pending' ? 'primary' : 'neutral'"
        :variant="submission.status === 'pending' ? 'subtle' : 'outline'"
        size="lg"
        block
      >
        {{ submission.status === "pending" ? "Проверить" : "Просмотр" }}
      </UButton>
    </td>
  </tr>
</template>
