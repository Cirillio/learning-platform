<script setup lang="ts">
import type { Lesson } from "~/types";

interface Props {
  lessons: Lesson[];
  durationWeeks?: number | null;
}

defineProps<Props>();
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-bold text-neutral-900 dark:text-white">
        Программа курса
      </h2>
      <span class="text-sm text-neutral-500"
        >{{ lessons.length }} уроков • {{ durationWeeks || "?" }} недель</span
      >
    </div>

    <div
      class="bg-white dark:bg-neutral-900 rounded-xl border border-neutral-200 dark:border-neutral-800 overflow-hidden"
    >
      <div v-if="lessons.length === 0" class="p-8 text-center text-neutral-500">
        Уроки пока не добавлены
      </div>

      <div
        v-for="(lesson, index) in lessons"
        :key="lesson.id"
        class="group border-b last:border-0 border-neutral-100 dark:border-neutral-800 hover:bg-neutral-50 dark:hover:bg-neutral-800/50 transition-colors"
      >
        <div class="p-4 sm:p-6 flex items-center gap-4">
          <!-- Icon/Number -->
          <div
            class="shrink-0 w-10 h-10 rounded-full bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center text-neutral-500 font-medium group-hover:bg-primary-50 group-hover:text-primary-600 transition-colors"
          >
            {{ index + 1 }}
          </div>

          <!-- Content -->
          <div class="grow min-w-0">
            <div
              class="flex flex-col sm:flex-row sm:items-center justify-between gap-2"
            >
              <h3
                class="font-medium text-neutral-900 dark:text-white truncate pr-4"
              >
                {{ lesson.title }}
              </h3>
              <div
                class="flex items-center gap-4 text-sm text-neutral-500 shrink-0"
              >
                <span v-if="lesson.duration_minutes"
                  >{{ lesson.duration_minutes }} мин</span
                >
                <span v-else>-- мин</span>
                <span class="hidden sm:inline text-neutral-300">|</span>
                <span class="hidden sm:inline">19:00 - 21:00</span>
                <!-- Mock time -->
              </div>
            </div>
            <p
              v-if="lesson.description"
              class="text-sm text-neutral-500 mt-1 line-clamp-1"
            >
              {{ lesson.description }}
            </p>
          </div>

          <!-- Arrow -->
          <UIcon
            name="i-heroicons-chevron-right"
            class="w-5 h-5 text-neutral-400 group-hover:text-neutral-600"
          />
        </div>
      </div>
    </div>
  </div>
</template>
