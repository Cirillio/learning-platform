<script setup lang="ts">
import type { Assignment } from "~/types";

defineProps<{
  assignment: Assignment;
  isDueDatePassed: boolean;
  courseSlug: string;
}>();

const emit = defineEmits<{
  (e: "delete"): void;
}>();
</script>

<template>
  <div class="flex items-start justify-between gap-4">
    <div class="flex-1">
      <div class="flex items-center gap-3 mb-2">
        <UBadge
          v-if="assignment.is_required"
          color="error"
          variant="soft"
          size="lg"
        >
          Обязательное
        </UBadge>
        <UBadge v-else color="neutral" variant="soft" size="lg">
          Необязательное
        </UBadge>
        <UBadge color="primary" variant="soft" size="lg">
          {{ assignment.max_score }} баллов
        </UBadge>
        <UBadge v-if="isDueDatePassed" color="error" variant="soft" size="lg">
          Срок истёк
        </UBadge>
      </div>
      <h1 class="text-3xl font-bold text-default mb-2">
        {{ assignment.title }}
      </h1>
      <p class="text-lg text-muted">
        {{ assignment.description }}
      </p>
    </div>
    <div class="flex gap-2 shrink-0">
      <UButton
        color="neutral"
        variant="ghost"
        icon="i-lucide-arrow-left"
        :to="`/teacher/courses/${courseSlug}/assignments`"
      >
        Назад
      </UButton>
      <UButton
        color="primary"
        icon="i-lucide-pencil"
        :to="`/teacher/courses/${courseSlug}/assignments/${assignment.id}/edit`"
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
