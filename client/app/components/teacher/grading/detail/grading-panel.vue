<script setup lang="ts">
import type { Grade } from "~/types";

defineProps<{
  gradeForm: {
    score: number;
    feedback: string;
  };
  maxScore: number;
  isGraded: boolean;
  isSubmitting: boolean;
  existingGrade: Grade | null;
}>();

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const formatDate = (date: string) => {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date));
};
</script>

<template>
  <div class="space-y-6">
    <!-- Grade Form -->
    <UCard class="sticky top-24">
      <template #header>
        <h2 class="text-lg font-semibold text-default">
          {{ isGraded ? "Оценка" : "Выставить оценку" }}
        </h2>
      </template>

      <form @submit.prevent="emit('submit')" class="space-y-2">
        <!-- Score Input -->
        <div>
          <label class="block text-xl font-medium text-default mb-2">
            Баллы (макс. {{ maxScore }})
          </label>
          <div class="flex items-center gap-3">
            <UInput
              size="xl"
              v-model.number="gradeForm.score"
              type="number"
              :min="0"
              :max="maxScore"
              class="w-24"
            />
            <span class="text-3xl font-bold text-default">/</span>
            <span class="text-3xl text-muted">{{ maxScore }}</span>
          </div>

          <!-- Quick Score Buttons -->
          <div class="flex gap-2 mt-3">
            <UButton
              v-for="percent in [100, 80, 60, 40]"
              :key="percent"
              size="md"
              color="neutral"
              variant="soft"
              @click="gradeForm.score = Math.round((maxScore * percent) / 100)"
            >
              {{ percent }}%
            </UButton>
          </div>
        </div>

        <!-- Feedback -->
        <div>
          <label class="block text-xl font-medium text-default mb-2">
            Комментарий (необязательно)
          </label>
          <UTextarea
            v-model="gradeForm.feedback"
            placeholder="Напишите комментарий для студента..."
            :rows="5"
            size="xl"
            class="w-full"
          />
        </div>

        <!-- Submit -->
        <UButton
          type="submit"
          color="primary"
          :loading="isSubmitting"
          block
          size="xl"
        >
          {{ isGraded ? "Обновить оценку" : "Выставить оценку" }}
        </UButton>
      </form>
    </UCard>

    <!-- Grade History (if graded) -->
    <div
      v-if="existingGrade"
      class="bg-success/5 border border-success/20 rounded-xl p-6"
    >
      <h3 class="font-semibold text-default mb-3 flex items-center gap-2">
        <UIcon name="i-lucide-check-circle" class="size-5 text-success" />
        Текущая оценка
      </h3>
      <div class="space-y-2 text-sm">
        <p class="text-default">
          <span class="text-muted">Балл:</span>
          <span class="font-semibold ml-2"
            >{{ existingGrade.score }}/{{ maxScore }}</span
          >
        </p>
        <p class="text-default">
          <span class="text-muted">Оценено:</span>
          <span class="ml-2">{{ formatDate(existingGrade.graded_at) }}</span>
        </p>
        <p class="text-default">
          <span class="text-muted">Проверил:</span>
          <span class="ml-2">{{ existingGrade.graded_by_name }}</span>
        </p>
      </div>
    </div>
  </div>
</template>
