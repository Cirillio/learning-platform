<script setup lang="ts">
import type { Assignment } from "~/types";

defineProps<{
  assignments: Assignment[];
  loading: boolean;
  slug: string;
}>();
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-semibold text-default">Задания курса</h2>
        <UButton
          :to="`/teacher/courses/${slug}/assignments/create`"
          icon="i-lucide-plus"
          color="primary"
          size="sm"
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
      <div
        v-for="assignment in assignments"
        :key="assignment.id"
        class="flex items-center gap-4 p-3 rounded-lg border border-default bg-elevated group hover:border-primary/50 transition-colors"
      >
        <div
          class="size-10 rounded-lg bg-warning/10 flex items-center justify-center shrink-0"
        >
          <UIcon name="i-lucide-clipboard-list" class="size-5 text-warning" />
        </div>

        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <h3 class="font-medium text-default">{{ assignment.title }}</h3>
            <UBadge
              v-if="assignment.is_required"
              color="error"
              variant="soft"
              size="sm"
            >
              Обязательное
            </UBadge>
          </div>
          <p class="text-sm text-muted truncate">
            {{ assignment.submissions_count }} сдач • Макс. балл:
            {{ assignment.max_score }}
          </p>
        </div>

        <div class="flex items-center gap-1">
          <UButton
            :to="`/teacher/courses/${slug}/grading?assignment=${assignment.id}`"
            icon="i-lucide-check-circle"
            color="success"
            variant="ghost"
            size="sm"
          />
          <UButton
            icon="i-lucide-pencil"
            color="neutral"
            variant="ghost"
            size="sm"
          />
        </div>
      </div>
    </div>
  </UCard>
</template>
