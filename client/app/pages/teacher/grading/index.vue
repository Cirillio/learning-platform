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
const currentPage = ref<number>(1);
const pageSize = 12;

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
      page: currentPage.value,
      page_size: pageSize,
    }),
  { watch: [statusFilter, assignmentFilter, currentPage] }
);

const submissions = computed(() => submissionsData.value?.results || []);
const totalCount = computed(() => submissionsData.value?.count || 0);
const pageCount = computed(() => Math.ceil(totalCount.value / pageSize));

// Reset page when filters change
watch([statusFilter, assignmentFilter], () => {
  currentPage.value = 1;
});

// SEO
useHead({
  title: "Проверка работ | Преподаватель",
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<template>
  <div>
    <!-- Header -->
    <TeacherGradingHeader
      :total-count="totalCount"
      :status-filter="statusFilter"
    />

    <!-- Filters -->
    <div class="flex w-full justify-between h-fit gap-2 items-center">
      <TeacherGradingFilters
        :status-filter="statusFilter"
        @update:status-filter="statusFilter = $event"
      />

      <UButton
        :disabled="pending"
        color="info"
        variant="outline"
        @click="() => refresh()"
      >
        Обновить</UButton
      >
    </div>

    <UPagination
      class="my-4"
      :disabled="pending"
      v-if="pageCount > 1"
      :items-per-page="pageSize"
      :total="totalCount"
      v-model:page="currentPage"
      show-edges
      :sibling-count="2"
    />
    <!-- Loading -->
    <Transition name="fade" mode="out-in">
      <div v-if="pending" key="loading" class="space-y-4">
        <USkeleton v-for="i in 5" :key="i" class="h-80 rounded-xl" />
      </div>

      <!-- Empty State -->
      <TeacherGradingEmptyState
        v-else-if="submissions.length === 0"
        key="empty"
        :status-filter="statusFilter"
      />

      <!-- Submissions Table -->
      <TeacherGradingTable v-else key="table" :submissions="submissions" />
    </Transition>
  </div>
</template>
