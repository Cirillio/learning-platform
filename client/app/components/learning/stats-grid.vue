<script setup lang="ts">
interface Props {
  progressPercent: number;
  completedLessons: number;
  totalLessons: number;
  assignmentsCount: number;
  courseSlug: string;
}

defineProps<Props>();
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
    <!-- Progress -->
    <div class="bg-elevated rounded-xl p-5 border border-default">
      <div class="flex items-center justify-between mb-3">
        <span class="text-sm text-muted">Прогресс</span>
        <UIcon name="i-lucide-trending-up" class="size-5 text-primary" />
      </div>
      <div class="text-2xl font-bold text-default mb-2">
        {{ progressPercent }}%
      </div>
      <UProgress :model-value="progressPercent" size="sm" color="primary" />
    </div>

    <!-- Lessons -->
    <div class="bg-elevated rounded-xl p-5 border border-default">
      <div class="flex items-center justify-between mb-3">
        <span class="text-sm text-muted">Уроки</span>
        <UIcon name="i-lucide-book-open" class="size-5 text-success" />
      </div>
      <div class="text-2xl font-bold text-default">
        {{ completedLessons }}/{{ totalLessons }}
      </div>
      <p class="text-xs text-muted mt-1">уроков пройдено</p>
    </div>

    <!-- Assignments -->
    <div class="bg-elevated rounded-xl p-5 border border-default">
      <div class="flex items-center justify-between mb-3">
        <span class="text-sm text-muted">Задания</span>
        <UIcon name="i-lucide-clipboard-check" class="size-5 text-warning" />
      </div>
      <div class="text-2xl font-bold text-default">
        {{ assignmentsCount }}
      </div>
      <NuxtLink
        :to="`/learning/${courseSlug}/assignments`"
        class="text-xs text-primary hover:underline mt-1 inline-block"
      >
        Посмотреть все →
      </NuxtLink>
    </div>
  </div>
</template>
