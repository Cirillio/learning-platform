<script setup lang="ts">
import type { Lesson } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Уроки курса",
});

const route = useRoute();
const api = useApi();
const toast = useToast();

const courseSlug = computed(() => route.params.slug as string);

// Fetch lessons
interface LessonsResponse {
  count: number;
  results: Lesson[];
}

const {
  data: lessonsData,
  refresh,
  status,
} = await useAsyncData<LessonsResponse>(
  `teacher-lessons-${courseSlug.value}`,
  () => api.get<LessonsResponse>("/lessons/", { course: courseSlug.value })
);

const lessons = computed(() =>
  [...(lessonsData.value?.results || [])].sort((a, b) => a.order - b.order)
);

// Stats
const stats = computed(() => ({
  total: lessons.value.length,
  published: lessons.value.filter((l) => l.is_published).length,
  draft: lessons.value.filter((l) => !l.is_published).length,
  totalDuration: lessons.value.reduce(
    (sum, l) => sum + (l.duration_minutes || 0),
    0
  ),
}));

// Reordering
const isReordering = ref(false);

const moveLesson = async (lesson: Lesson, direction: "up" | "down") => {
  const currentIndex = lessons.value.findIndex((l) => l.id === lesson.id);
  if (
    (direction === "up" && currentIndex === 0) ||
    (direction === "down" && currentIndex === lessons.value.length - 1)
  ) {
    return;
  }

  const targetIndex = direction === "up" ? currentIndex - 1 : currentIndex + 1;
  const targetLesson = lessons.value[targetIndex];

  if (!targetLesson) return;

  isReordering.value = true;
  try {
    // Swap orders
    await Promise.all([
      api.patch(`/lessons/${lesson.slug}/`, { order: targetLesson.order }),
      api.patch(`/lessons/${targetLesson.slug}/`, { order: lesson.order }),
    ]);

    await refresh();
    toast.add({
      title: "Порядок обновлён",
      color: "success",
    });
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: "Не удалось изменить порядок",
      color: "error",
    });
  } finally {
    isReordering.value = false;
  }
};

// Toggle publish
const togglePublish = async (lesson: Lesson) => {
  try {
    await api.patch(`/lessons/${lesson.slug}/`, {
      is_published: !lesson.is_published,
    });
    await refresh();
    toast.add({
      title: lesson.is_published ? "Урок скрыт" : "Урок опубликован",
      color: "success",
    });
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: e.data?.detail || "Не удалось изменить статус",
      color: "error",
    });
  }
};

// Delete lesson
const lessonToDelete = ref<Lesson | null>(null);
const isDeleteModalOpen = ref(false);
const isDeleting = ref(false);

const openDeleteModal = (lesson: Lesson) => {
  lessonToDelete.value = lesson;
  isDeleteModalOpen.value = true;
};

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false;
  lessonToDelete.value = null;
};

const confirmDelete = async () => {
  if (!lessonToDelete.value) return;

  isDeleting.value = true;
  try {
    await api.delete(`/lessons/${lessonToDelete.value.slug}/`);
    toast.add({
      title: "Урок удалён",
      color: "success",
    });
    closeDeleteModal();
    await refresh();
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: e.data?.detail || "Не удалось удалить урок",
      color: "error",
    });
  } finally {
    isDeleting.value = false;
  }
};

// Helpers
const formatDuration = (minutes: number | null): string => {
  if (!minutes) return "—";
  if (minutes < 60) return `${minutes} мин`;
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return mins > 0 ? `${hours}ч ${mins}мин` : `${hours}ч`;
};

const getLessonTypeIcon = (type: string): string => {
  const icons: Record<string, string> = {
    video: "i-lucide-play-circle",
    text: "i-lucide-file-text",
    quiz: "i-lucide-help-circle",
    assignment: "i-lucide-clipboard-list",
  };
  return icons[type] || "i-lucide-file";
};

const getLessonTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    video: "Видео",
    text: "Текст",
    quiz: "Тест",
    assignment: "Задание",
  };
  return labels[type] || type;
};

// SEO
useHead({
  title: "Уроки курса | Преподаватель",
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
        <h1 class="text-2xl font-bold text-default">Уроки курса</h1>
        <p class="text-muted mt-1">Управление содержимым курса</p>
      </div>

      <UButton
        :to="`/teacher/courses/${courseSlug}/lessons/create`"
        color="primary"
        icon="i-lucide-plus"
      >
        Добавить урок
      </UButton>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-elevated rounded-xl border border-default p-4">
        <div class="text-2xl font-bold text-default">{{ stats.total }}</div>
        <div class="text-sm text-muted">Всего уроков</div>
      </div>
      <div class="bg-elevated rounded-xl border border-default p-4">
        <div class="text-2xl font-bold text-success">{{ stats.published }}</div>
        <div class="text-sm text-muted">Опубликовано</div>
      </div>
      <div class="bg-elevated rounded-xl border border-default p-4">
        <div class="text-2xl font-bold text-warning">{{ stats.draft }}</div>
        <div class="text-sm text-muted">Черновиков</div>
      </div>
      <div class="bg-elevated rounded-xl border border-default p-4">
        <div class="text-2xl font-bold text-info">
          {{ formatDuration(stats.totalDuration) }}
        </div>
        <div class="text-sm text-muted">Общая длительность</div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="status === 'pending'" class="space-y-3">
      <USkeleton v-for="i in 5" :key="i" class="h-20 rounded-xl" />
    </div>

    <!-- Empty State -->
    <UEmpty
      v-else-if="lessons.length === 0"
      icon="i-lucide-book-open"
      title="Уроков пока нет"
      description="Создайте первый урок для вашего курса"
    >
      <template #actions>
        <UButton
          :to="`/teacher/courses/${courseSlug}/lessons/create`"
          color="primary"
          icon="i-lucide-plus"
        >
          Создать урок
        </UButton>
      </template>
    </UEmpty>

    <!-- Lessons List -->
    <div v-else class="space-y-3">
      <div
        v-for="(lesson, index) in lessons"
        :key="lesson.id"
        class="bg-elevated rounded-xl border border-default p-4 hover:border-primary/30 transition-colors"
        :class="{ 'opacity-50': isReordering }"
      >
        <div class="flex items-center gap-4">
          <!-- Order Controls -->
          <div class="flex flex-col gap-1">
            <UButton
              color="neutral"
              variant="ghost"
              size="xs"
              icon="i-lucide-chevron-up"
              :disabled="index === 0 || isReordering"
              @click="moveLesson(lesson, 'up')"
            />
            <UButton
              color="neutral"
              variant="ghost"
              size="xs"
              icon="i-lucide-chevron-down"
              :disabled="index === lessons.length - 1 || isReordering"
              @click="moveLesson(lesson, 'down')"
            />
          </div>

          <!-- Order Number -->
          <div
            class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center shrink-0"
          >
            <span class="text-lg font-bold text-primary">{{
              lesson.order
            }}</span>
          </div>

          <!-- Lesson Info -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <h3 class="font-semibold text-default truncate">
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

            <div class="flex flex-wrap items-center gap-3 text-sm text-muted">
              <div class="flex items-center gap-1.5">
                <UIcon name="i-lucide-video" class="size-4" />
                <span>Видео</span>
              </div>

              <div
                v-if="lesson.duration_minutes"
                class="flex items-center gap-1.5"
              >
                <UIcon name="i-lucide-clock" class="size-4" />
                <span>{{ formatDuration(lesson.duration_minutes) }}</span>
              </div>

              <div
                v-if="lesson.materials_count"
                class="flex items-center gap-1.5"
              >
                <UIcon name="i-lucide-paperclip" class="size-4" />
                <span>{{ lesson.materials_count }} материалов</span>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="flex items-center gap-2">
            <UTooltip :text="lesson.is_published ? 'Скрыть' : 'Опубликовать'">
              <UButton
                :color="lesson.is_published ? 'success' : 'neutral'"
                variant="ghost"
                :icon="
                  lesson.is_published ? 'i-lucide-eye' : 'i-lucide-eye-off'
                "
                size="sm"
                @click="togglePublish(lesson)"
              />
            </UTooltip>

            <UDropdownMenu
              :items="[
                [
                  {
                    label: 'Редактировать',
                    icon: 'i-lucide-edit',
                    to: `/teacher/courses/${courseSlug}/lessons/${lesson.slug}/edit`,
                  },
                  {
                    label: 'Предпросмотр',
                    icon: 'i-lucide-external-link',
                    to: `/learning/${courseSlug}/lessons/${lesson.slug}`,
                    target: '_blank',
                  },
                ],
                [
                  {
                    label: 'Удалить',
                    icon: 'i-lucide-trash-2',
                    color: 'error' as const,
                    click: () => openDeleteModal(lesson),
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
    </div>

    <!-- Tips -->
    <div class="mt-8 p-4 bg-info/5 border border-info/20 rounded-xl">
      <div class="flex items-start gap-3">
        <UIcon
          name="i-lucide-lightbulb"
          class="size-5 text-info shrink-0 mt-0.5"
        />
        <div class="text-sm text-muted">
          <p class="font-medium text-default mb-1">Советы по организации</p>
          <ul class="list-disc list-inside space-y-1">
            <li>Используйте стрелки для изменения порядка уроков</li>
            <li>Уроки-черновики не видны студентам</li>
            <li>Рекомендуемая длительность одного урока — 10-20 минут</li>
          </ul>
        </div>
      </div>
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
              <h3 class="text-lg font-semibold text-default">Удалить урок?</h3>
              <p class="text-sm text-muted">«{{ lessonToDelete?.title }}»</p>
            </div>
          </div>

          <p class="text-muted mb-6">
            Это действие нельзя отменить. Все связанные материалы и задания
            также будут удалены.
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
