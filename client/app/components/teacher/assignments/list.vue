<script setup lang="ts">
import type { Assignment, Lesson } from "~/types";

interface Props {
  assignments: Assignment[];
  lessons: Lesson[];
  courseSlug: string;
  isLoading?: boolean;
}

interface Emits {
  (e: "edit", assignment: Assignment): void;
  (e: "delete", assignment: Assignment): void;
  (e: "view-submissions", assignment: Assignment): void;
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
});

const emit = defineEmits<Emits>();

// Filter state
const selectedLesson = ref<string | null>(null);
const searchQuery = ref("");

// Lesson options for filter
const lessonOptions = computed(() => [
  { label: "Все уроки", value: null },
  ...props.lessons.map((l) => ({
    label: `${l.order}. ${l.title}`,
    value: l.slug,
  })),
]);

// Filtered assignments
const filteredAssignments = computed(() => {
  let result = props.assignments;

  // Filter by lesson
  if (selectedLesson.value) {
    result = result.filter((a) => a.lesson === selectedLesson.value);
  }

  // Filter by search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(
      (a) =>
        a.title.toLowerCase().includes(query) ||
        a.description?.toLowerCase().includes(query)
    );
  }

  return result;
});

// Get lesson title by slug
const getLessonTitle = (lessonSlug: string) => {
  const lesson = props.lessons.find((l) => l.slug === lessonSlug);
  return lesson ? `${lesson.order}. ${lesson.title}` : lessonSlug;
};

// Delete confirmation modal
const deleteModal = ref(false);
const assignmentToDelete = ref<Assignment | null>(null);

const openDeleteModal = (assignment: Assignment) => {
  assignmentToDelete.value = assignment;
  deleteModal.value = true;
};

const confirmDelete = () => {
  if (assignmentToDelete.value) {
    emit("delete", assignmentToDelete.value);
  }
  deleteModal.value = false;
  assignmentToDelete.value = null;
};

// Actions dropdown
const getActions = (assignment: Assignment) => [
  [
    {
      label: "Редактировать",
      icon: "i-heroicons-pencil-square",
      click: () => emit("edit", assignment),
    },
    {
      label: "Ответы студентов",
      icon: "i-heroicons-document-text",
      click: () => emit("view-submissions", assignment),
    },
  ],
  [
    {
      label: "Удалить",
      icon: "i-heroicons-trash",
      color: "error" as const,
      click: () => openDeleteModal(assignment),
    },
  ],
];

// Format date
const formatDate = (dateString: string | null | undefined) => {
  if (!dateString) return "Без срока";
  return new Date(dateString).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

// Check if assignment is overdue
const isOverdue = (assignment: Assignment) => {
  if (!assignment.due_date) return false;
  return new Date(assignment.due_date) < new Date();
};
</script>

<template>
  <div class="space-y-4">
    <!-- Filters -->
    <div class="flex flex-col sm:flex-row gap-3">
      <UInput
        v-model="searchQuery"
        placeholder="Поиск по названию..."
        class="flex-1"
      >
        <template #leading>
          <UIcon name="i-heroicons-magnifying-glass" class="text-muted" />
        </template>
      </UInput>
      <USelect
        v-model="selectedLesson"
        :items="lessonOptions"
        placeholder="Фильтр по уроку"
        class="w-full sm:w-64"
      />
    </div>

    <!-- Loading skeleton -->
    <template v-if="isLoading">
      <div v-for="i in 3" :key="i" class="animate-pulse">
        <div class="bg-elevated rounded-lg p-4 border border-default">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-muted rounded-lg" />
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-muted rounded w-1/3" />
              <div class="h-3 bg-muted rounded w-2/3" />
              <div class="h-3 bg-muted rounded w-1/4" />
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Empty state -->
    <UEmpty
      v-else-if="filteredAssignments.length === 0"
      icon="i-heroicons-clipboard-document-list"
      :title="
        searchQuery || selectedLesson ? 'Ничего не найдено' : 'Нет заданий'
      "
      :description="
        searchQuery || selectedLesson
          ? 'Попробуйте изменить параметры поиска'
          : 'Создайте первое задание для курса'
      "
    />

    <!-- Assignments list -->
    <div v-else class="space-y-3">
      <div
        v-for="assignment in filteredAssignments"
        :key="assignment.id"
        class="group bg-elevated rounded-lg border border-default hover:border-primary/30 transition-all duration-200"
      >
        <div class="flex items-start gap-4 p-4">
          <!-- Icon -->
          <div
            class="shrink-0 w-12 h-12 rounded-lg flex items-center justify-center"
            :class="
              assignment.is_required
                ? 'bg-primary/10 text-primary'
                : 'bg-muted text-muted'
            "
          >
            <UIcon
              name="i-heroicons-clipboard-document-check"
              class="w-6 h-6"
            />
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <h3 class="font-medium text-default truncate">
                {{ assignment.title }}
              </h3>
              <UBadge
                v-if="assignment.is_required"
                color="primary"
                variant="subtle"
                size="xs"
              >
                Обязательное
              </UBadge>
            </div>

            <p class="text-sm text-muted mb-2">
              {{ getLessonTitle(assignment.lesson) }}
            </p>

            <div class="flex flex-wrap items-center gap-4 text-xs text-muted">
              <span class="flex items-center gap-1">
                <UIcon name="i-heroicons-star" class="w-3.5 h-3.5" />
                {{ assignment.max_score }} баллов
              </span>
              <span
                class="flex items-center gap-1"
                :class="isOverdue(assignment) ? 'text-error' : ''"
              >
                <UIcon name="i-heroicons-calendar" class="w-3.5 h-3.5" />
                {{ formatDate(assignment.due_date) }}
              </span>
              <span class="flex items-center gap-1">
                <UIcon name="i-heroicons-document-text" class="w-3.5 h-3.5" />
                {{ assignment.submissions_count }} ответов
              </span>
              <span
                v-if="assignment.allow_late_submission"
                class="flex items-center gap-1"
              >
                <UIcon name="i-heroicons-clock" class="w-3.5 h-3.5" />
                Поздняя сдача
              </span>
            </div>
          </div>

          <!-- Actions -->
          <div
            class="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <UButton
              icon="i-heroicons-pencil-square"
              variant="ghost"
              color="neutral"
              size="sm"
              @click="emit('edit', assignment)"
            />
            <UButton
              icon="i-heroicons-document-text"
              variant="ghost"
              color="neutral"
              size="sm"
              @click="emit('view-submissions', assignment)"
            >
              <template #trailing>
                <UBadge
                  v-if="assignment.submissions_count > 0"
                  :label="String(assignment.submissions_count)"
                  size="xs"
                />
              </template>
            </UButton>
            <UDropdownMenu :items="getActions(assignment)">
              <UButton
                icon="i-heroicons-ellipsis-vertical"
                variant="ghost"
                color="neutral"
                size="sm"
              />
            </UDropdownMenu>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete confirmation modal -->
    <UModal v-model:open="deleteModal">
      <template #content>
        <div class="p-6">
          <div class="flex items-center gap-4 mb-4">
            <div class="p-3 rounded-full bg-error/10">
              <UIcon
                name="i-heroicons-exclamation-triangle"
                class="w-6 h-6 text-error"
              />
            </div>
            <div>
              <h3 class="font-semibold text-lg">Удалить задание?</h3>
              <p class="text-muted text-sm">
                Задание "{{ assignmentToDelete?.title }}" будет удалено вместе
                со всеми ответами студентов
              </p>
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <UButton
              variant="ghost"
              color="neutral"
              @click="deleteModal = false"
            >
              Отмена
            </UButton>
            <UButton color="error" @click="confirmDelete"> Удалить </UButton>
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>
