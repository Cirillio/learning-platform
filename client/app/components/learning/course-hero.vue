<script setup lang="ts">
import type { CourseDetail } from "~/types";

interface Props {
  course: CourseDetail;
  courseSlug: string;
  nextLessonSlug?: string;
  completedLessons: number;
}

const props = defineProps<Props>();

const difficultyLabel = computed(() => {
  const labels: Record<string, string> = {
    beginner: "Начальный",
    intermediate: "Средний",
    advanced: "Продвинутый",
  };
  return labels[props.course.difficulty] || props.course.difficulty;
});

const difficultyColor = computed(() => {
  const colors: Record<string, "success" | "warning" | "error"> = {
    beginner: "success",
    intermediate: "warning",
    advanced: "error",
  };
  return colors[props.course.difficulty] || "neutral";
});
</script>

<template>
  <div
    class="relative rounded-2xl bg-linear-to-br from-primary/20 to-primary/5 p-6 lg:p-8 mb-8 overflow-hidden"
  >
    <div class="absolute inset-0 bg-grid-pattern opacity-5" />
    <div
      class="relative z-10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6"
    >
      <div class="space-y-4">
        <div class="flex items-center gap-2">
          <UBadge color="primary" variant="subtle">
            {{ course.category?.name || "Курс" }}
          </UBadge>
          <UBadge :color="difficultyColor" variant="subtle">
            {{ difficultyLabel }}
          </UBadge>
        </div>
        <h1 class="text-2xl lg:text-3xl font-bold text-default">
          {{ course.title }}
        </h1>
        <p class="text-muted max-w-2xl">
          {{ course.short_description }}
        </p>
      </div>

      <!-- Continue Button -->
      <div v-if="nextLessonSlug" class="shrink-0">
        <UButton
          :to="`/learning/${courseSlug}/lessons/${nextLessonSlug}`"
          size="lg"
          color="primary"
          icon="i-lucide-play"
          class="shadow-lg"
        >
          {{ completedLessons > 0 ? "Продолжить" : "Начать обучение" }}
        </UButton>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bg-grid-pattern {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cg fill='%239C92AC' fill-opacity='0.2'%3E%3Cpath d='M0 0h40v40H0V0zm1 1v38h38V1H1z'/%3E%3C/g%3E%3C/svg%3E");
}
</style>
