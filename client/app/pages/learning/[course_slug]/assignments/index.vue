<script setup lang="ts">
import type {
  Assignment,
  Lesson,
  LessonDetail,
  PaginatedResponse,
} from "~/types";

definePageMeta({
  layout: "default",
  middleware: ["auth", "enrolled-course"],
});

const route = useRoute();
const courseSlug = computed(() => route.params.course_slug as string);
const lessonFilter = computed(() => route.query.lesson as string | undefined);

// Service placeholder - will be implemented
const api = useApi();

// Fetch assignments
const { data: assignmentsResponse, pending } = await useAsyncData<
  PaginatedResponse<Assignment>
>(
  `learning-assignments-${courseSlug.value}`,
  () =>
    api.get<PaginatedResponse<Assignment>>("/assignments/", {
      course: courseSlug.value,
      lesson: lessonFilter.value,
    }),
  { watch: [lessonFilter] }
);

const { data: lessonData, pending: lessonPending } =
  await useAsyncData<LessonDetail | null>(
    `learning-lesson-${lessonFilter.value}`,
    async () => {
      if (!lessonFilter.value) return null;
      const resp = api.get<LessonDetail>(`/lessons/${lessonFilter.value}/`);
      resp.then((r) => {
        console.log({ ...r });
      });
      return resp;
    },

    {
      watch: [lessonFilter],
    }
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
  <LayoutContainer class="bg-default py-6 flex-1 space-y-2">
    <!-- Header -->
    <div>
      <div class="flex items-center gap-2 mb-2">
        <UButton
          :to="`/learning/${courseSlug}`"
          color="primary"
          variant="soft"
          icon="heroicons:arrow-left"
        />
        <UIcon name="i-lucide-clipboard-list" class="size-8 text-primary" />
        <h1 class="text-4xl font-bold text-default">Задания курса</h1>
      </div>
      <p class="text-lg text-muted">
        Выполняйте задания для закрепления материала и получения оценок
      </p>
    </div>

    <!-- Filters -->
    <div>
      <UTabs
        size="lg"
        :items="filterOptions.map((f) => ({ label: f.label, value: f.value }))"
        v-model="activeFilter"
        class="w-fit"
      />
    </div>

    <!-- Lesson info (when lesson is selected) -->
    <div v-if="lessonFilter">
      <USkeleton v-if="lessonPending" class="h-40 rounded-xl" />

      <UCard v-else-if="lessonData">
        <div class="flex items-start gap-4">
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between">
              <div>
                <h4 class="text-2xl font-semibold text-default">
                  {{ lessonData.title }}
                </h4>
                <p class="text-base text-muted mt-3 line-clamp-4">
                  {{
                    lessonData.description ||
                    (lessonData.content
                      ? lessonData.content.slice(0, 240) +
                        (lessonData.content.length > 240 ? "..." : "")
                      : "")
                  }}
                </p>
              </div>
              <div class="text-right text-sm text-muted">
                <div>Длительность: {{ lessonData.duration_minutes }} мин</div>
                <div>Материалов: {{ lessonData.materials?.length || 0 }}</div>
                <div>Заданий: {{ lessonData.assignments_count ?? 0 }}</div>
              </div>
            </div>

            <div class="mt-4 flex items-center gap-3">
              <UButton
                v-if="lessonData.slug"
                :to="`/learning/${courseSlug}/lessons/${lessonData.slug}`"
                color="primary"
                size="md"
                icon="i-lucide-arrow-right"
              >
                Открыть урок
              </UButton>

              <UButton
                v-if="lessonData.materials && lessonData.materials.length > 0"
                color="neutral"
                variant="ghost"
                size="md"
                :to="`/learning/${courseSlug}/lessons/${lessonData.slug}#materials`"
              >
                Материалы ({{ lessonData.materials.length }})
              </UButton>
            </div>
          </div>
        </div>
      </UCard>

      <USeparator class="my-6" />
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
              <div class="flex items-center gap-2">
                <h3
                  class="text-2xl font-semibold text-default group-hover:text-primary transition-colors"
                >
                  {{ assignment.title }}
                </h3>
                <UBadge
                  v-if="assignment.is_submitted"
                  color="success"
                  variant="subtle"
                >
                  Сдано
                </UBadge>
                <UBadge
                  v-else-if="isOverdue(assignment.due_date)"
                  color="error"
                  variant="subtle"
                >
                  Просрочено
                </UBadge>
                <UBadge
                  v-else-if="assignment.is_required"
                  color="warning"
                  variant="subtle"
                >
                  Обязательное
                </UBadge>
              </div>

              <!-- Description -->
              <p class="text-lg text-muted line-clamp-2 my-2">
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
  </LayoutContainer>
</template>
