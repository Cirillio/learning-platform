<script setup lang="ts">
import type { Submission, Assignment } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Проверка работ",
});

const route = useRoute();
const api = useApi();

// Filters
const statusFilter = ref<string>((route.query.status as string) || "pending");
const assignmentFilter = ref<string>((route.query.assignment as string) || "");

// Fetch submissions
interface SubmissionsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Submission[];
}

const {
  data: submissionsData,
  pending,
  refresh,
} = await useAsyncData<SubmissionsResponse>(
  "teacher-grading-submissions",
  () =>
    api.get<SubmissionsResponse>("/submissions/", {
      status: statusFilter.value !== "all" ? statusFilter.value : undefined,
      assignment: assignmentFilter.value || undefined,
    }),
  { watch: [statusFilter, assignmentFilter] }
);

const submissions = computed(() => submissionsData.value?.results || []);
const totalCount = computed(() => submissionsData.value?.count || 0);

// Filter options
const statusOptions = [
  { label: "На проверке", value: "pending" },
  { label: "Оценено", value: "graded" },
  { label: "Все", value: "all" },
];

// SEO
useHead({
  title: "Проверка работ | Преподаватель",
});
</script>

<template>
  <div>
    <!-- Header -->
    <TeacherGradingHeader
      :total-count="totalCount"
      :status-filter="statusFilter"
    />

    <!-- Filters -->
    <TeacherGradingFilters
      :status-filter="statusFilter"
      @update:status-filter="statusFilter = $event"
    />

    <!-- Loading -->
    <div v-if="pending" class="space-y-4">
      <USkeleton v-for="i in 5" :key="i" class="h-24 rounded-xl" />
    </div>

    <!-- Empty State -->
    <TeacherGradingEmptyState
      v-else-if="submissions.length === 0"
      :status-filter="statusFilter"
    />

    <!-- Submissions Table -->
    <TeacherGradingTable v-else :submissions="submissions" />
  </div>
</template>
