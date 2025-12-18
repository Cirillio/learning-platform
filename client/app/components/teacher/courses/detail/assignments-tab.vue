<script setup lang="ts">
import type { Assignment } from "~/types";

defineProps<{
  assignments: Assignment[];
  loading: boolean;
  slug: string;
}>();

const emit = defineEmits<{
  (e: "edit", assignment: Assignment): void;
  (e: "delete", assignment: Assignment): void;
}>();

// Форматирование даты
const formatDueDate = (dateString: string | null | undefined): string => {
  if (!dateString) return "Без срока";
  const date = new Date(dateString);
  return date.toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
};
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-semibold text-default">Задания курса</h2>
        <UButton
          :to="`/teacher/courses/${slug}/assignments/create`"
          icon="i-lucide-plus"
          color="primary"
          size="lg"
        >
          Добавить задание
        </UButton>
      </div>
    </template>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3">
      <USkeleton v-for="i in 4" :key="i" class="h-20 rounded-xl" />
    </div>

    <!-- Empty -->
    <div v-else-if="assignments.length === 0" class="text-center py-8">
      <UIcon
        name="i-lucide-clipboard-x"
        class="size-12 text-muted mx-auto mb-3"
      />
      <p class="text-muted mb-4">Заданий пока нет</p>
      <UButton
        :to="`/teacher/courses/${slug}/assignments/create`"
        icon="i-lucide-plus"
        color="primary"
      >
        Добавить задание
      </UButton>
    </div>

    <!-- List -->
    <div v-else class="space-y-3">
      <TeacherCoursesDetailListItem
        v-for="assignment in assignments"
        :key="assignment.id"
        :desc="`${assignment.submissions_count} сдач • Макс. балл: ${assignment.max_score}`"
        :subdesc="formatDueDate(assignment.due_date)"
        :link="`/teacher/courses/${slug}/assignments/${assignment.id}`"
        @edit="emit('edit', assignment)"
        @delete="emit('delete', assignment)"
      >
        <template #leading>
          <div
            class="size-12 rounded-lg bg-warning/10 flex items-center justify-center shrink-0"
          >
            <UIcon name="i-lucide-clipboard-list" class="size-6 text-warning" />
          </div>
        </template>

        <template #title>
          <div class="flex items-center gap-2">
            <h3 class="font-medium text-xl text-default">
              {{ assignment.title }}
            </h3>
            <UBadge
              v-if="assignment.is_required"
              color="error"
              variant="soft"
              size="sm"
            >
              Обязательное
            </UBadge>
          </div>
        </template>
      </TeacherCoursesDetailListItem>
    </div>
  </UCard>
</template>
