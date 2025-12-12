<script setup lang="ts">
import type { LessonNavigation } from "~/types";

interface Props {
  navigation: LessonNavigation | null;
  isCompleted: boolean;
  isCompleting: boolean;
}

defineProps<Props>();

const emit = defineEmits<{
  previous: [];
  next: [];
  complete: [];
}>();
</script>

<template>
  <UCard class="dark:bg-muted/25 bg-muted/75">
    <div
      class="flex flex-col sm:flex-row items-center w-full justify-between gap-4"
    >
      <!-- Previous Lesson -->
      <UButton
        v-if="navigation?.previous"
        variant="subtle"
        color="secondary"
        icon="i-lucide-arrow-left"
        class="w-full sm:w-auto"
        @click="emit('previous')"
      >
        <span class="truncate max-w-[150px]">
          {{ navigation.previous.title }}
        </span>
      </UButton>

      <!-- Complete / Progress Info -->
      <div class="flex items-center gap-3">
        <span v-if="navigation" class="text-sm text-muted hidden sm:block">
          Урок {{ navigation.current_index + 1 }} из
          {{ navigation.total_lessons }}
        </span>

        <!-- TODO: implement complete lesson functionality -->

        <!-- <UButton
          v-if="!isCompleted"
          color="success"
          variant="solid"
          icon="i-lucide-check-circle"
          :loading="isCompleting"
          :disabled="isCompleting"
          @click="emit('complete')"
        >
          Завершить урок
        </UButton> -->
        <!-- 
        <UBadge
          v-else
          color="success"
          variant="soft"
          icon="i-lucide-check"
          size="lg"
        >
          Урок завершён
        </UBadge> -->
      </div>

      <!-- Next Lesson -->
      <UButton
        v-if="navigation?.next"
        variant="solid"
        color="primary"
        trailing-icon="i-lucide-arrow-right"
        class="w-full sm:w-auto"
        @click="emit('next')"
      >
        <span class="truncate max-w-[150px]">
          {{ navigation.next.title }}
        </span>
      </UButton>
      <UButton
        v-else
        :to="`/courses/${$route.params.slug}`"
        variant="outline"
        color="neutral"
        trailing-icon="i-lucide-layout-grid"
        class="w-full sm:w-auto"
      >
        К курсу
      </UButton>
    </div>
  </UCard>
</template>
