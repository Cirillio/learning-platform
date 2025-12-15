<script setup lang="ts">
import type { Grade } from "~/types";

defineProps<{
  grade: Grade;
  maxScore: number;
}>();

const formatDate = (date: string | null | undefined): string => {
  if (!date) return "";
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
  <div class="bg-success/5 border border-success/20 rounded-xl p-6 lg:p-8">
    <h2 class="text-lg font-semibold text-default mb-4 flex items-center gap-2">
      <UIcon name="i-lucide-check-circle" class="size-5 text-success" />
      Результат проверки
    </h2>
    <div class="space-y-4">
      <div class="flex items-center gap-4">
        <span class="text-muted">Оценка:</span>
        <span class="text-2xl font-bold text-success">
          {{ grade.score }}/{{ maxScore }}
        </span>
      </div>
      <div v-if="grade.feedback">
        <span class="text-muted block mb-2">Комментарий преподавателя:</span>
        <div class="bg-muted ring ring-muted rounded-lg p-4 text-default">
          {{ grade.feedback }}
        </div>
      </div>
      <div class="text-sm text-muted">
        Проверено: {{ formatDate(grade.graded_at) }} ({{
          grade.graded_by_name
        }})
      </div>
    </div>
  </div>
</template>
