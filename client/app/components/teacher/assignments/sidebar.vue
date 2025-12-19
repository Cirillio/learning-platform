<script setup lang="ts">
import type { Assignment, LessonDetail } from "~/types";
import { formatDate } from "~/utils/formatters.util";

defineProps<{
  assignment: Assignment;
  isDueDatePassed: boolean;
  courseSlug: string;
  lesson?: LessonDetail | null;
}>();
</script>

<template>
  <div class="space-y-6">
    <!-- Info Card -->
    <UCard>
      <template #header>
        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-info" class="size-5 text-primary" />
          <h3 class="font-semibold">Информация</h3>
        </div>
      </template>
      <div class="space-y-4 text-sm">
        <div class="flex justify-between items-center">
          <span class="text-muted">Макс. балл</span>
          <span class="font-semibold">{{ assignment.max_score }}</span>
        </div>
        <USeparator />
        <div class="flex justify-between items-center">
          <span class="text-muted">Срок сдачи</span>
          <span
            :class="isDueDatePassed ? 'text-error font-semibold' : 'font-semibold'"
          >
            {{ formatDate(assignment.due_date) }}
          </span>
        </div>
        <USeparator />
        <div class="flex justify-between items-center">
          <span class="text-muted">Поздняя сдача</span>
          <UBadge
            :color="assignment.allow_late_submission ? 'success' : 'error'"
            variant="soft"
            size="sm"
          >
            {{ assignment.allow_late_submission ? "Разрешена" : "Запрещена" }}
          </UBadge>
        </div>
        <USeparator />
        <div class="flex justify-between items-center">
          <span class="text-muted">Обязательное</span>
          <UBadge
            :color="assignment.is_required ? 'error' : 'neutral'"
            variant="soft"
            size="sm"
          >
            {{ assignment.is_required ? "Да" : "Нет" }}
          </UBadge>
        </div>
        <USeparator />
        <div class="flex justify-between items-center">
          <span class="text-muted">Создано</span>
          <span class="font-medium">{{
            new Date(assignment.created_at).toLocaleDateString("ru-RU")
          }}</span>
        </div>
      </div>
    </UCard>

    <!-- Quick Actions -->
    <UCard>
      <template #header>
        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-zap" class="size-5 text-primary" />
          <h3 class="font-semibold">Быстрые действия</h3>
        </div>
      </template>
      <div class="space-y-2">
        <UButton
          :to="`/teacher/courses/${courseSlug}/assignments/${assignment.id}/edit`"
          color="neutral"
          variant="soft"
          icon="i-lucide-pencil"
          block
        >
          Редактировать задание
        </UButton>
        <UButton
          v-if="lesson"
          :to="`/teacher/courses/${courseSlug}/lessons/${lesson.slug}`"
          color="neutral"
          variant="soft"
          icon="i-lucide-book-open"
          block
        >
          Перейти к уроку
        </UButton>
        <UButton
          :to="`/teacher/courses/${courseSlug}/assignments`"
          color="neutral"
          variant="ghost"
          icon="i-lucide-list"
          block
        >
          Все задания курса
        </UButton>
      </div>
    </UCard>
  </div>
</template>
