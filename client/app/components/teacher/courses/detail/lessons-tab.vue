<script setup lang="ts">
import type { Lesson } from "~/types";

defineProps<{
  lessons: Lesson[];
  loading: boolean;
  slug: string;
}>();

const emit = defineEmits<{
  (e: "add"): void;
  (e: "delete", lessonId: number): void;
}>();
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-semibold text-default">Уроки курса</h2>
        <UButton
          icon="i-lucide-plus"
          color="primary"
          size="sm"
          @click="emit('add')"
        >
          Добавить урок
        </UButton>
      </div>
    </template>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3">
      <USkeleton v-for="i in 4" :key="i" class="h-20 rounded-xl" />
    </div>

    <!-- Empty -->
    <div v-else-if="lessons.length === 0" class="text-center py-8">
      <UIcon name="i-lucide-book-x" class="size-12 text-muted mx-auto mb-3" />
      <p class="text-muted mb-4">Уроков пока нет</p>
      <UButton icon="i-lucide-plus" color="primary" @click="emit('add')">
        Добавить первый урок
      </UButton>
    </div>

    <!-- List -->
    <div v-else class="space-y-3">
      <div
        v-for="lesson in lessons"
        :key="lesson.id"
        class="flex items-center gap-4 p-3 rounded-lg border border-default bg-elevated group hover:border-primary/50 transition-colors"
      >
        <!-- Order -->
        <div
          class="size-10 rounded-lg bg-primary/10 flex items-center justify-center font-semibold text-primary shrink-0"
        >
          {{ lesson.order }}
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <h3 class="font-medium text-default">{{ lesson.title }}</h3>
            <UBadge
              v-if="!lesson.is_published"
              color="warning"
              variant="soft"
              size="sm"
            >
              Черновик
            </UBadge>
          </div>
          <p class="text-sm text-muted truncate">{{ lesson.description }}</p>
        </div>

        <!-- Duration -->
        <div class="text-sm text-muted shrink-0">
          {{ lesson.duration_minutes }} мин
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-1">
          <UButton
            :to="`/teacher/courses/${slug}/lessons/${lesson.slug}`"
            icon="i-lucide-pencil"
            color="neutral"
            variant="ghost"
            size="sm"
          />
          <UButton
            icon="i-lucide-trash-2"
            color="error"
            variant="ghost"
            size="sm"
            @click="emit('delete', lesson.id)"
          />
        </div>
      </div>
    </div>
  </UCard>
</template>
