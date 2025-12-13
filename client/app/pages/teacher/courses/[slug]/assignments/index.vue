<script setup lang="ts">
import type { Assignment, Lesson } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Задания курса",
});

const route = useRoute();
const api = useApi();
const toast = useToast();

const courseSlug = computed(() => route.params.slug as string);

// Fetch lessons for lesson names
interface LessonsResponse {
  count: number;
  results: Lesson[];
}

const { data: lessonsData } = await useAsyncData<LessonsResponse>(
  `teacher-course-lessons-for-assignments-${courseSlug.value}`,
  () => api.get<LessonsResponse>("/lessons/", { course: courseSlug.value })
);

const lessonsMap = computed(() => {
  const map = new Map<string, Lesson>();
  lessonsData.value?.results.forEach((l) => map.set(l.slug, l));
  return map;
});

// Fetch course assignments
interface AssignmentsResponse {
  count: number;
  results: Assignment[];
}

const {
  data: assignmentsData,
  refresh,
  status,
} = await useAsyncData<AssignmentsResponse>(
  `teacher-assignments-${courseSlug.value}`,
  () =>
    api.get<AssignmentsResponse>("/assignments/", { course: courseSlug.value })
);

const assignments = computed(() => assignmentsData.value?.results || []);

// Group by lesson
const groupedByLesson = computed(() => {
  const grouped = new Map<string, Assignment[]>();

  assignments.value.forEach((assignment) => {
    const lessonSlug = assignment.lesson || "no-lesson";
    if (!grouped.has(lessonSlug)) {
      grouped.set(lessonSlug, []);
    }
    grouped.get(lessonSlug)!.push(assignment);
  });

  return grouped;
});

// Stats
const stats = computed(() => {
  const total = assignments.value.length;
  const required = assignments.value.filter((a) => a.is_required).length;
  const withDeadline = assignments.value.filter((a) => a.due_date).length;
  const totalSubmissions = assignments.value.reduce(
    (sum, a) => sum + (a.submissions_count || 0),
    0
  );

  return { total, required, withDeadline, totalSubmissions };
});

// Delete assignment
const assignmentToDelete = ref<Assignment | null>(null);
const isDeleteModalOpen = ref(false);
const isDeleting = ref(false);

const openDeleteModal = (assignment: Assignment) => {
  assignmentToDelete.value = assignment;
  isDeleteModalOpen.value = true;
};

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false;
  assignmentToDelete.value = null;
};

const confirmDelete = async () => {
  if (!assignmentToDelete.value) return;

  isDeleting.value = true;
  try {
    await api.delete(`/assignments/${assignmentToDelete.value.id}/`);
    toast.add({
      title: "Задание удалено",
      color: "success",
    });
    closeDeleteModal();
    await refresh();
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: e.data?.detail || "Не удалось удалить задание",
      color: "error",
    });
  } finally {
    isDeleting.value = false;
  }
};

// Helpers
const formatDate = (date: string | null): string => {
  if (!date) return "—";
  return new Date(date).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const isOverdue = (dueDate: string | null): boolean => {
  if (!dueDate) return false;
  return new Date(dueDate) < new Date();
};

// SEO
useHead({
  title: "Задания курса | Преподаватель",
});
</script>

<template>
  <div>
    <!-- Header -->
    <div
      class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8"
    >
      <div>
        <NuxtLink
          :to="`/teacher/courses/${courseSlug}`"
          class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors mb-2"
        >
          <UIcon name="i-lucide-arrow-left" class="size-4" />
          К курсу
        </NuxtLink>
        <h1 class="text-2xl font-bold text-default">Задания курса</h1>
        <p class="text-muted mt-1">
          Всего {{ stats.total }}
          {{ stats.total === 1 ? "задание" : "заданий" }}
        </p>
      </div>

      <UButton
        :to="`/teacher/courses/${courseSlug}/assignments/create`"
        color="primary"
        icon="i-lucide-plus"
      >
        Добавить задание
      </UButton>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-elevated rounded-xl border border-default p-4">
        <div class="text-2xl font-bold text-default">{{ stats.total }}</div>
        <div class="text-sm text-muted">Всего заданий</div>
      </div>
      <div class="bg-elevated rounded-xl border border-default p-4">
        <div class="text-2xl font-bold text-warning">{{ stats.required }}</div>
        <div class="text-sm text-muted">Обязательных</div>
      </div>
      <div class="bg-elevated rounded-xl border border-default p-4">
        <div class="text-2xl font-bold text-info">{{ stats.withDeadline }}</div>
        <div class="text-sm text-muted">С дедлайном</div>
      </div>
      <div class="bg-elevated rounded-xl border border-default p-4">
        <div class="text-2xl font-bold text-success">
          {{ stats.totalSubmissions }}
        </div>
        <div class="text-sm text-muted">Сдано работ</div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="status === 'pending'" class="space-y-4">
      <USkeleton v-for="i in 3" :key="i" class="h-24 rounded-xl" />
    </div>

    <!-- Empty State -->
    <UEmpty
      v-else-if="assignments.length === 0"
      icon="i-lucide-clipboard-list"
      title="Заданий пока нет"
      description="Создайте первое задание для вашего курса"
    >
      <template #actions>
        <UButton
          :to="`/teacher/courses/${courseSlug}/assignments/create`"
          color="primary"
          icon="i-lucide-plus"
        >
          Создать задание
        </UButton>
      </template>
    </UEmpty>

    <!-- Assignments List -->
    <div v-else class="space-y-6">
      <template
        v-for="[lessonSlug, lessonAssignments] in groupedByLesson"
        :key="lessonSlug"
      >
        <!-- Lesson Header -->
        <div class="flex items-center gap-3 mb-3">
          <UIcon name="i-lucide-book-open" class="size-5 text-muted" />
          <h2 class="font-semibold text-default">
            {{ lessonsMap.get(lessonSlug)?.title || "Без урока" }}
          </h2>
          <UBadge color="neutral" variant="subtle">
            {{ lessonAssignments.length }}
          </UBadge>
        </div>

        <!-- Assignments -->
        <div class="grid gap-4">
          <div
            v-for="assignment in lessonAssignments"
            :key="assignment.id"
            class="bg-elevated rounded-xl border border-default p-5 hover:border-primary/30 transition-colors"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-2">
                  <h3 class="font-semibold text-default truncate">
                    {{ assignment.title }}
                  </h3>
                  <UBadge
                    v-if="assignment.is_required"
                    color="warning"
                    variant="subtle"
                    size="xs"
                  >
                    Обязательное
                  </UBadge>
                </div>

                <p
                  v-if="assignment.description"
                  class="text-sm text-muted mb-3 line-clamp-2"
                >
                  {{ assignment.description }}
                </p>

                <div class="flex flex-wrap items-center gap-4 text-sm">
                  <div class="flex items-center gap-1.5 text-muted">
                    <UIcon name="i-lucide-star" class="size-4" />
                    <span>{{ assignment.max_score }} баллов</span>
                  </div>

                  <div
                    v-if="assignment.due_date"
                    class="flex items-center gap-1.5"
                    :class="
                      isOverdue(assignment.due_date)
                        ? 'text-error'
                        : 'text-muted'
                    "
                  >
                    <UIcon name="i-lucide-calendar" class="size-4" />
                    <span>{{ formatDate(assignment.due_date) }}</span>
                    <UBadge
                      v-if="isOverdue(assignment.due_date)"
                      color="error"
                      variant="subtle"
                      size="xs"
                    >
                      Просрочено
                    </UBadge>
                  </div>

                  <div class="flex items-center gap-1.5 text-muted">
                    <UIcon name="i-lucide-users" class="size-4" />
                    <span>{{ assignment.submissions_count || 0 }} работ</span>
                  </div>
                </div>
              </div>

              <!-- Actions -->
              <UDropdownMenu
                :items="[
                  [
                    {
                      label: 'Редактировать',
                      icon: 'i-lucide-edit',
                      to: `/teacher/courses/${courseSlug}/assignments/${assignment.id}/edit`,
                    },
                    {
                      label: 'Посмотреть работы',
                      icon: 'i-lucide-eye',
                      to: `/teacher/grading?assignment=${assignment.id}`,
                    },
                  ],
                  [
                    {
                      label: 'Удалить',
                      icon: 'i-lucide-trash-2',
                      color: 'error' as const,
                      click: () => openDeleteModal(assignment),
                    },
                  ],
                ]"
              >
                <UButton
                  color="neutral"
                  variant="ghost"
                  icon="i-lucide-more-vertical"
                  size="sm"
                />
              </UDropdownMenu>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Delete Modal -->
    <UModal v-model:open="isDeleteModalOpen">
      <template #content>
        <div class="p-6">
          <div class="flex items-center gap-4 mb-4">
            <div
              class="w-12 h-12 rounded-full bg-error/10 flex items-center justify-center"
            >
              <UIcon name="i-lucide-alert-triangle" class="size-6 text-error" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-default">
                Удалить задание?
              </h3>
              <p class="text-sm text-muted">
                «{{ assignmentToDelete?.title }}»
              </p>
            </div>
          </div>

          <p class="text-muted mb-6">
            Это действие нельзя отменить. Все связанные работы студентов также
            будут удалены.
          </p>

          <div class="flex items-center justify-end gap-3">
            <UButton color="neutral" variant="ghost" @click="closeDeleteModal">
              Отмена
            </UButton>
            <UButton color="error" :loading="isDeleting" @click="confirmDelete">
              Удалить
            </UButton>
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>
