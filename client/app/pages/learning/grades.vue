<script setup lang="ts">
import type { Grade } from "~/types";

definePageMeta({
  layout: "default",
  middleware: ["auth", "student-only"],
});

const api = useApi();

// Filters
const currentPage = ref(1);
const pageSize = 10;

// Fetch grades
interface GradesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Grade[];
}

const {
  data: gradesData,
  pending,
  refresh,
} = await useAsyncData<GradesResponse>(
  "student-grades",
  () =>
    api.get<GradesResponse>("/grades/", {
      page: currentPage.value,
      page_size: pageSize,
    }),
  { watch: [currentPage] }
);

const grades = computed(() => gradesData.value?.results || []);
const totalCount = computed(() => gradesData.value?.count || 0);
const pageCount = computed(() => Math.ceil(totalCount.value / pageSize));

// Statistics
const stats = computed(() => {
  if (!grades.value.length) return null;

  const scores = grades.value.map((g) => g.score);
  const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
  const max = Math.max(...scores);
  const min = Math.min(...scores);

  return {
    total: totalCount.value,
    average: Math.round(avg * 10) / 10,
    max,
    min,
  };
});

// Score color
const getScoreColor = (score: number): string => {
  if (score >= 90) return "text-success";
  if (score >= 70) return "text-primary";
  if (score >= 50) return "text-warning";
  return "text-error";
};

const getScoreBadgeColor = (
  score: number
): "success" | "primary" | "warning" | "error" => {
  if (score >= 90) return "success";
  if (score >= 70) return "primary";
  if (score >= 50) return "warning";
  return "error";
};

// Format date
const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
};

// SEO
useHead({
  title: "Мои оценки | Обучение",
});
</script>

<template>
  <LayoutContainer class="py-8 bg-default">
    <!-- Header -->
    <div class="mb-2">
      <div class="flex items-center gap-2 mb-2">
        <UIcon name="i-lucide-trophy" class="size-8 text-primary" />
        <h1 class="text-2xl lg:text-3xl font-bold text-default">Мои оценки</h1>
      </div>
      <p class="text-muted">
        История всех полученных оценок за выполненные задания
      </p>
    </div>

    <!-- Stats Cards -->
    <div
      v-if="stats && !pending"
      class="grid grid-cols-2 md:grid-cols-4 gap-2 mb-2"
    >
      <UCard :ui="{ body: 'p-4' }">
        <div class="text-center">
          <p class="text-2xl font-bold text-default">{{ stats.total }}</p>
          <p class="text-sm text-muted">Всего оценок</p>
        </div>
      </UCard>
      <UCard :ui="{ body: 'p-4' }">
        <div class="text-center">
          <p class="text-2xl font-bold text-primary">{{ stats.average }}</p>
          <p class="text-sm text-muted">Средний балл</p>
        </div>
      </UCard>
      <UCard :ui="{ body: 'p-4' }">
        <div class="text-center">
          <p class="text-2xl font-bold text-success">{{ stats.max }}</p>
          <p class="text-sm text-muted">Лучший балл</p>
        </div>
      </UCard>
      <UCard :ui="{ body: 'p-4' }">
        <div class="text-center">
          <p class="text-2xl font-bold text-warning">{{ stats.min }}</p>
          <p class="text-sm text-muted">Минимальный балл</p>
        </div>
      </UCard>
    </div>

    <!-- Loading -->
    <div v-if="pending" class="space-y-2">
      <USkeleton v-for="i in 5" :key="i" class="h-24 rounded-xl" />
    </div>

    <!-- Empty State -->
    <UCard v-else-if="grades.length === 0" :ui="{ body: 'p-12 text-center' }">
      <UIcon
        name="i-lucide-clipboard-check"
        class="size-16 text-muted mx-auto mb-4"
      />
      <h2 class="text-xl font-semibold text-default mb-2">Оценок пока нет</h2>
      <p class="text-muted mb-6">
        Выполняйте задания на курсах, чтобы получить оценки
      </p>
      <UButton to="/courses" color="primary"> Перейти к курсам </UButton>
    </UCard>

    <!-- Grades List -->
    <div v-else class="space-y-2">
      <UCard v-for="grade in grades" :key="grade.id" :ui="{ body: 'p-0' }">
        <div class="flex flex-col md:flex-row md:items-center gap-4 p-4">
          <!-- Score Badge -->
          <div class="shrink-0">
            <UBadge
              :color="getScoreBadgeColor(grade.score)"
              size="lg"
              variant="subtle"
              :ui="{ base: 'px-4 py-2 text-lg font-bold' }"
            >
              {{ grade.score }}
            </UBadge>
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <h3 class="font-semibold text-default truncate">
              {{ grade.assignment_title }}
            </h3>
            <p class="text-sm text-muted mt-1">
              Проверил: {{ grade.graded_by_name }}
            </p>
            <p class="text-xs text-muted">
              {{ formatDate(grade.graded_at) }}
            </p>
          </div>

          <!-- Feedback -->
          <div v-if="grade.feedback" class="md:max-w-xs">
            <UTooltip :text="grade.feedback" :delay="100">
              <div
                class="flex items-center gap-2 text-sm text-muted cursor-help"
              >
                <UIcon name="i-lucide-message-square" class="size-4" />
                <span class="truncate max-w-[200px]">{{ grade.feedback }}</span>
              </div>
            </UTooltip>
          </div>
        </div>

        <!-- Expanded Feedback -->
        <div
          v-if="grade.feedback"
          class="px-4 pb-4 pt-0 border-t border-default mt-2"
        >
          <p class="text-sm text-muted italic">
            <span class="font-medium">Комментарий:</span> {{ grade.feedback }}
          </p>
        </div>
      </UCard>
    </div>

    <!-- Pagination -->
    <div v-if="pageCount > 1" class="flex justify-center mt-8">
      <UPagination
        v-model:page="currentPage"
        :total="totalCount"
        :items-per-page="pageSize"
        show-edges
        :sibling-count="2"
      />
    </div>
  </LayoutContainer>
</template>
