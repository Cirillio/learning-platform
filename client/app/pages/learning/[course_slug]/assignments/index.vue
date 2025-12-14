<script setup lang="ts">
import type { Assignment } from "~/types";

definePageMeta({
  layout: "learning",
  middleware: ["auth", "enrolled-course"],
});

const route = useRoute();
const courseSlug = computed(() => route.params.course_slug as string);
const lessonFilter = computed(() => route.query.lesson as string | undefined);

// Service placeholder - will be implemented
const api = useApi();

interface AssignmentsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Assignment[];
}

// Fetch assignments
const { data: assignmentsResponse, pending } =
  await useAsyncData<AssignmentsResponse>(
    `learning-assignments-${courseSlug.value}`,
    () =>
      api.get<AssignmentsResponse>("/assignments/", {
        course: courseSlug.value,
        lesson: lessonFilter.value,
      }),
    { watch: [lessonFilter] }
  );

const assignments = computed(() => assignmentsResponse.value?.results || []);

// Filter tabs
const filterOptions = [
  { label: "Все", value: "all" },
  { label: "Не сдано", value: "pending" },
  { label: "На проверке", value: "submitted" },
  { label: "Оценено", value: "graded" },
];

const activeFilter = ref("all");

const filteredAssignments = computed(() => {
  if (activeFilter.value === "all") return assignments.value;

  return assignments.value.filter((a) => {
    if (activeFilter.value === "pending") return !a.is_submitted;
    if (activeFilter.value === "submitted") return a.is_submitted;
    // For graded - would need additional field
    return true;
  });
});

// Helpers
const isOverdue = (dueDate: string | null | undefined): boolean => {
  if (!dueDate) return false;
  return new Date(dueDate) < new Date();
};

const formatDate = (date: string | null | undefined): string => {
  if (!date) return "Без срока";
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date));
};

const getDaysUntilDue = (dueDate: string | null | undefined): number | null => {
  if (!dueDate) return null;
  const diff = new Date(dueDate).getTime() - Date.now();
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
};

// SEO
useHead({
  title: "Задания | Обучение",
});
</script>

<template>
  <div class="space-y-2">
    <!-- Header -->
    <div>
      <div class="flex items-center gap-2 mb-2">
        <UIcon name="i-lucide-clipboard-list" class="size-6 text-primary" />
        <h1 class="text-2xl font-bold text-default">Задания курса</h1>
      </div>
      <p class="text-base text-muted">
        Выполняйте задания для закрепления материала и получения оценок
      </p>
    </div>

    <!-- Filters -->
    <div>
      <UTabs
        :items="filterOptions.map((f) => ({ label: f.label, value: f.value }))"
        v-model="activeFilter"
        class="w-fit"
      />
    </div>

    <!-- Loading -->
    <div v-if="pending" class="space-y-2">
      <USkeleton v-for="i in 4" :key="i" class="h-32 rounded-xl" />
    </div>

    <!-- Empty State -->
    <div
      v-else-if="filteredAssignments.length === 0"
      class="flex flex-col items-center justify-center py-20 gap-2"
    >
      <UIcon name="i-lucide-clipboard-x" class="size-16 text-muted" />
      <h2 class="text-2xl font-bold text-default">Заданий пока нет</h2>
      <p class="text-base text-muted">
        {{
          activeFilter === "all"
            ? "К этому курсу пока не добавлены задания"
            : "Нет заданий с выбранным статусом"
        }}
      </p>
    </div>

    <!-- Assignments List -->
    <div v-else class="space-y-2">
      <NuxtLink
        v-for="assignment in filteredAssignments"
        :key="assignment.id"
        :to="`/learning/${courseSlug}/assignments/${assignment.id}`"
        class="block"
      >
        <UCard
          :ui="{ body: 'p-3' }"
          class="hover:border-primary/50 transition-all group"
        >
          <div class="flex items-start justify-between gap-2">
            <div class="flex-1 min-w-0">
              <!-- Title & Status -->
              <div class="flex items-center gap-2 mb-2">
                <h3
                  class="text-base font-semibold text-default group-hover:text-primary transition-colors"
                >
                  {{ assignment.title }}
                </h3>
                <UBadge
                  v-if="assignment.is_submitted"
                  color="success"
                  variant="subtle"
                  size="sm"
                >
                  Сдано
                </UBadge>
                <UBadge
                  v-else-if="isOverdue(assignment.due_date)"
                  color="error"
                  variant="subtle"
                  size="sm"
                >
                  Просрочено
                </UBadge>
                <UBadge
                  v-else-if="assignment.is_required"
                  color="warning"
                  variant="subtle"
                  size="sm"
                >
                  Обязательное
                </UBadge>
              </div>

              <!-- Description -->
              <p class="text-base text-muted line-clamp-2 mb-2">
                {{ assignment.description }}
              </p>

              <!-- Meta Info -->
              <div class="flex items-center gap-2 text-base text-muted">
                <!-- Due Date -->
                <div class="flex items-center gap-2">
                  <UIcon name="i-lucide-calendar" class="size-4" />
                  <span
                    :class="
                      isOverdue(assignment.due_date) && !assignment.is_submitted
                        ? 'text-error'
                        : ''
                    "
                  >
                    {{ formatDate(assignment.due_date) }}
                  </span>
                  <template
                    v-if="
                      assignment.due_date &&
                      !assignment.is_submitted &&
                      !isOverdue(assignment.due_date)
                    "
                  >
                    <span class="text-warning">
                      ({{ getDaysUntilDue(assignment.due_date) }} дн.)
                    </span>
                  </template>
                </div>

                <!-- Max Score -->
                <div class="flex items-center gap-2">
                  <UIcon name="i-lucide-star" class="size-4" />
                  <span>Макс. балл: {{ assignment.max_score }}</span>
                </div>

                <!-- Files -->
                <div
                  v-if="assignment.files.length > 0"
                  class="flex items-center gap-2"
                >
                  <UIcon name="i-lucide-paperclip" class="size-4" />
                  <span>{{ assignment.files.length }} файл(ов)</span>
                </div>
              </div>
            </div>

            <!-- Arrow -->
            <UIcon
              name="i-lucide-chevron-right"
              class="size-5 text-muted group-hover:text-primary transition-colors shrink-0 mt-1"
            />
          </div>
        </UCard>
      </NuxtLink>
    </div>
  </div>
</template>
