<script setup lang="ts">
import type { Lesson } from "~/types";

interface Props {
  lessons: Lesson[];
  courseSlug: string;
  isLoading?: boolean;
}

interface Emits {
  (e: "edit", lesson: Lesson): void;
  (e: "delete", lesson: Lesson): void;
  (e: "toggle-publish", lesson: Lesson): void;
  (e: "reorder", lessonSlug: string, newOrder: number): void;
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
});

const emit = defineEmits<Emits>();

// Sort lessons by order
const sortedLessons = computed(() =>
  [...props.lessons].sort((a, b) => a.order - b.order)
);

// Delete confirmation modal
const deleteModal = ref(false);
const lessonToDelete = ref<Lesson | null>(null);

const openDeleteModal = (lesson: Lesson) => {
  lessonToDelete.value = lesson;
  deleteModal.value = true;
};

const confirmDelete = () => {
  if (lessonToDelete.value) {
    emit("delete", lessonToDelete.value);
  }
  deleteModal.value = false;
  lessonToDelete.value = null;
};

// Actions dropdown
const getActions = (lesson: Lesson) => [
  [
    {
      label: "Редактировать",
      icon: "i-heroicons-pencil-square",
      click: () => emit("edit", lesson),
    },
    {
      label: lesson.is_published ? "Снять с публикации" : "Опубликовать",
      icon: lesson.is_published ? "i-heroicons-eye-slash" : "i-heroicons-eye",
      click: () => emit("toggle-publish", lesson),
    },
  ],
  [
    {
      label: "Удалить",
      icon: "i-heroicons-trash",
      color: "error" as const,
      click: () => openDeleteModal(lesson),
    },
  ],
];

// Format duration
const formatDuration = (minutes: number) => {
  if (minutes < 60) return `${minutes} мин`;
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return mins > 0 ? `${hours} ч ${mins} мин` : `${hours} ч`;
};
</script>

<template>
  <div class="space-y-4">
    <!-- Loading skeleton -->
    <template v-if="isLoading">
      <div v-for="i in 3" :key="i" class="animate-pulse">
        <div class="bg-elevated rounded-lg p-4 border border-default">
          <div class="flex items-center gap-4">
            <div class="w-8 h-8 bg-muted rounded" />
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-muted rounded w-1/3" />
              <div class="h-3 bg-muted rounded w-2/3" />
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Empty state -->
    <UEmpty
      v-else-if="sortedLessons.length === 0"
      icon="i-heroicons-academic-cap"
      title="Нет уроков"
      description="Создайте первый урок для этого курса"
    />

    <!-- Lessons list -->
    <div v-else class="space-y-3">
      <div
        v-for="lesson in sortedLessons"
        :key="lesson.id"
        class="group bg-elevated rounded-lg border border-default hover:border-primary/30 transition-all duration-200"
      >
        <div class="flex items-center gap-4 p-4">
          <!-- Order number -->
          <div
            class="shrink-0 w-10 h-10 rounded-lg flex items-center justify-center font-semibold text-lg"
            :class="
              lesson.is_published
                ? 'bg-primary/10 text-primary'
                : 'bg-muted text-muted'
            "
          >
            {{ lesson.order }}
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <h3 class="font-medium text-default truncate">
                {{ lesson.title }}
              </h3>
              <UBadge
                v-if="!lesson.is_published"
                color="warning"
                variant="subtle"
                size="xs"
              >
                Черновик
              </UBadge>
            </div>
            <p v-if="lesson.description" class="text-sm text-muted truncate">
              {{ lesson.description }}
            </p>
            <div class="flex items-center gap-4 mt-2 text-xs text-muted">
              <span class="flex items-center gap-1">
                <UIcon name="i-heroicons-clock" class="w-3.5 h-3.5" />
                {{ formatDuration(lesson.duration_minutes) }}
              </span>
              <span v-if="lesson.video_url" class="flex items-center gap-1">
                <UIcon name="i-heroicons-video-camera" class="w-3.5 h-3.5" />
                Видео
              </span>
              <span class="flex items-center gap-1">
                <UIcon name="i-heroicons-document" class="w-3.5 h-3.5" />
                {{ lesson.materials_count }} материалов
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
              @click="emit('edit', lesson)"
            />
            <UDropdownMenu :items="getActions(lesson)">
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
              <h3 class="font-semibold text-lg">Удалить урок?</h3>
              <p class="text-muted text-sm">
                Урок "{{ lessonToDelete?.title }}" будет удалён безвозвратно
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
