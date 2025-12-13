<script setup lang="ts">
import type { Assignment, Grade } from "~/types";

const props = defineProps<{
  assignment: Assignment;
  grade?: Grade | null;
  isGraded: boolean;
  isPending: boolean;
  isOverdue: boolean;
  hasSubmission: boolean;
}>();

const formatDate = (date: string | null | undefined): string => {
  if (!date) return "Без срока";
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
  <div class="bg-elevated rounded-xl border border-default p-6 lg:p-8">
    <div class="flex items-start justify-between gap-4 mb-6">
      <div>
        <div class="flex items-center gap-3 mb-2">
          <h1 class="text-2xl font-bold text-default">
            {{ assignment.title }}
          </h1>
          <UBadge v-if="isGraded" color="success" variant="subtle">
            Оценено
          </UBadge>
          <UBadge v-else-if="isPending" color="warning" variant="subtle">
            На проверке
          </UBadge>
          <UBadge v-else-if="isOverdue" color="error" variant="subtle">
            Просрочено
          </UBadge>
        </div>
        <p class="text-muted">{{ assignment.description }}</p>
      </div>

      <!-- Score Display -->
      <div
        v-if="isGraded && grade"
        class="text-center px-6 py-4 bg-success/10 rounded-xl shrink-0"
      >
        <div class="text-3xl font-bold text-success">
          {{ grade.score }}/{{ assignment.max_score }}
        </div>
        <div class="text-sm text-muted">Оценка</div>
      </div>
    </div>

    <!-- Meta Info -->
    <div class="flex flex-wrap items-center gap-6 text-sm text-muted">
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-calendar" class="size-4" />
        <span>Срок сдачи: </span>
        <span
          :class="[
            isOverdue && !hasSubmission ? 'text-error font-medium' : '',
            !isOverdue && assignment.due_date ? 'text-default' : '',
          ]"
        >
          {{ formatDate(assignment.due_date) }}
        </span>
      </div>
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-star" class="size-4" />
        <span>Макс. балл: {{ assignment.max_score }}</span>
      </div>
      <UBadge
        v-if="assignment.is_required"
        color="error"
        variant="soft"
        size="sm"
      >
        Обязательное
      </UBadge>
      <UBadge
        v-if="assignment.allow_late_submission"
        color="info"
        variant="soft"
        size="sm"
      >
        Можно сдать позже срока
      </UBadge>
    </div>
  </div>
</template>
