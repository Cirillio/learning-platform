<script setup lang="ts">
import type { Lesson } from "~/types";

interface Props {
  lessons: Lesson[];
  courseSlug: string;
  durationWeeks?: number | null;
}

defineProps<Props>();
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-baseline justify-between mr-2">
      <h2 class="text-4xl font-bold text-default">Программа курса</h2>
      <span class="text-lg text-muted"
        >{{ lessons.length }} уроков • {{ durationWeeks || "?" }} недель</span
      >
    </div>

    <div class="bg-default rounded-lg border border-default overflow-hidden">
      <div v-if="lessons.length === 0" class="p-8 text-center text-muted">
        Уроки пока не добавлены
      </div>

      <div
        v-for="(lesson, index) in lessons"
        :key="lesson.id"
        class="group border-b bg-muted/25 last:border-0 border-default hover:bg-muted/50 transition-colors cursor-pointer"
      >
        <NuxtLink
          :to="`/courses/${courseSlug}/lessons/${lesson.slug}`"
          class="block p-3"
        >
          <div class="flex items-center gap-3">
            <!-- Icon/Number -->
            <div
              class="shrink-0 size-10 rounded-full bg-muted flex items-center justify-center text-muted font-medium transition-colors"
            >
              {{ index + 1 }}
            </div>

            <!-- Content -->
            <div class="grow min-w-0">
              <div
                class="flex flex-col sm:flex-row sm:items-center justify-between gap-2"
              >
                <h3 class="font-semibold text-default text-xl truncate pr-4">
                  {{ lesson.title }}
                </h3>
              </div>
              <p
                v-if="lesson.description"
                class="text-lg text-muted line-clamp-1"
              >
                {{ lesson.description }}
              </p>

              <USeparator class="my-2 w-2/3" />

              <div
                class="flex items-center gap-4 text-base text-muted shrink-0"
              >
                <span v-if="lesson.duration_minutes"
                  >{{ lesson.duration_minutes }} мин</span
                >
                <span v-else>-- мин</span>
              </div>
            </div>

            <!-- Arrow -->
            <div
              class="rounded-full bg-elevated dark:bg-muted/25 flex py-1 pr-3 pl-1 group-hover:bg-primary group-hover:pr-0.5 group-hover:pl-3.5 transition-all duration-150 ease-in-out"
            >
              <UIcon
                name="i-lucide-chevron-right"
                class="size-6 group-hover:bg-black dark:bg-white/50 bg-black/50 transition-all"
              />
            </div>
          </div>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
