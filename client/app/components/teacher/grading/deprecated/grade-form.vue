<script setup lang="ts">
import { z } from "zod";

interface Props {
  maxScore: number;
  currentScore?: number;
  currentFeedback?: string;
  isGraded?: boolean;
  loading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  currentScore: 0,
  currentFeedback: "",
  isGraded: false,
  loading: false,
});

const emit = defineEmits<{
  submit: [data: { score: number; feedback: string }];
}>();

// Form state
const score = ref(props.currentScore);
const feedback = ref(props.currentFeedback);

// Validation
const gradeSchema = z.object({
  score: z
    .number()
    .min(0, "Оценка не может быть отрицательной")
    .max(props.maxScore, `Оценка не может превышать ${props.maxScore}`),
  feedback: z.string().max(5000, "Комментарий слишком длинный"),
});

// Watch for prop changes
watch(
  () => props.currentScore,
  (val) => {
    score.value = val;
  }
);

watch(
  () => props.currentFeedback,
  (val) => {
    feedback.value = val || "";
  }
);

// Computed
const scorePercent = computed(() => {
  if (props.maxScore === 0) return 0;
  return Math.round((score.value / props.maxScore) * 100);
});

const scoreColor = computed(() => {
  if (scorePercent.value >= 80) return "success";
  if (scorePercent.value >= 60) return "warning";
  return "error";
});

// Quick score buttons
const quickScores = [100, 80, 60, 40, 20, 0];

const setQuickScore = (percent: number) => {
  score.value = Math.round((props.maxScore * percent) / 100);
};

// Submit
const handleSubmit = () => {
  const result = gradeSchema.safeParse({
    score: score.value,
    feedback: feedback.value,
  });

  if (!result.success) {
    return;
  }

  emit("submit", {
    score: score.value,
    feedback: feedback.value,
  });
};
</script>

<template>
  <div class="bg-elevated rounded-xl border border-default overflow-hidden">
    <div class="px-6 py-4 border-b border-default">
      <h3 class="text-lg font-semibold text-default">
        {{ isGraded ? "Редактировать оценку" : "Выставить оценку" }}
      </h3>
    </div>

    <div class="p-6">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Score Input -->
        <div>
          <label class="block text-sm font-medium text-default mb-3">
            Баллы
          </label>

          <!-- Score Display -->
          <div class="flex items-center gap-4 mb-4">
            <UInput
              v-model.number="score"
              type="number"
              :min="0"
              :max="maxScore"
              class="w-28 text-center font-semibold text-lg"
            />
            <span class="text-2xl text-muted">/</span>
            <span class="text-2xl font-bold text-default">{{ maxScore }}</span>
            <UBadge :color="scoreColor" variant="soft" size="lg" class="ml-2">
              {{ scorePercent }}%
            </UBadge>
          </div>

          <!-- Score Slider -->
          <UProgress
            :model-value="scorePercent"
            :color="scoreColor"
            size="sm"
            class="mb-4"
          />

          <!-- Quick Score Buttons -->
          <div class="flex flex-wrap gap-2">
            <UButton
              v-for="percent in quickScores"
              :key="percent"
              size="sm"
              :color="scorePercent === percent ? 'primary' : 'neutral'"
              :variant="scorePercent === percent ? 'solid' : 'soft'"
              @click="setQuickScore(percent)"
            >
              {{ percent }}%
            </UButton>
          </div>
        </div>

        <!-- Feedback -->
        <div>
          <label class="block text-sm font-medium text-default mb-2">
            Комментарий для студента
          </label>
          <UTextarea
            v-model="feedback"
            placeholder="Напишите комментарий о работе студента..."
            :rows="5"
            class="w-full"
          />
          <p class="text-xs text-muted mt-1">
            Необязательно, но полезно для студента
          </p>
        </div>

        <!-- Submit -->
        <UButton
          type="submit"
          color="primary"
          size="lg"
          :loading="loading"
          class="w-full"
        >
          <UIcon name="i-lucide-check-circle" class="size-5 mr-2" />
          {{ isGraded ? "Обновить оценку" : "Выставить оценку" }}
        </UButton>
      </form>
    </div>
  </div>
</template>
