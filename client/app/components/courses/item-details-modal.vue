<script lang="ts" setup>
import type { Course } from "~/types";

interface Props {
  course: Course;
}

const props = defineProps<Props>();

const isOpen = defineModel<boolean>("open");

// Получаем маркер сложности с цветовой индикацией
const difficultyBadge = computed(() => {
  const badges = {
    beginner: { label: "Начальный", color: "success" as const },
    intermediate: { label: "Средний", color: "warning" as const },
    advanced: { label: "Продвинутый", color: "accent" as const },
  };
  return badges[props.course.difficulty] || badges.beginner;
});

// Получаем статус курса
const statusBadge = computed(() => {
  const statuses = {
    draft: { label: "Черновик", color: "neutral" as const },
    published: { label: "Опубликован", color: "success" as const },
    archived: { label: "Архив", color: "neutral" as const },
  };
  return statuses[props.course.status] || statuses.draft;
});

// Формируем URL изображения обложки с fallback
const coverImage = computed(
  () =>
    props.course.cover_image_url ||
    "https://images.steamusercontent.com/ugc/2079019457927111911/45068F1A462AF6EB757ADABDD621AB5FDE49E38E/?imw=512&amp;imh=512&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true"
);

// Форматирование даты
const formattedDate = computed(() => {
  return new Date(props.course.created_at).toLocaleDateString("ru-RU", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
});

// Обновленная дата
const updatedDate = computed(() => {
  return new Date(props.course.updated_at).toLocaleDateString("ru-RU", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
});
</script>

<template>
  <UModal
    v-model:open="isOpen"
    :title="course.title"
    :ui="{
      content: 'max-w-4xl',
      body: 'space-y-6',
      footer: 'justify-between',
    }"
  >
    <template #body>
      <!-- Обложка курса -->
      <div class="relative aspect-video rounded-lg overflow-hidden">
        <img
          :src="coverImage"
          :alt="course.title"
          class="w-full h-full object-cover"
        />
        <div
          class="absolute top-4 right-4 flex gap-2 bg-elevated/80 backdrop-blur-sm p-2 rounded-lg"
        >
          <UBadge :color="statusBadge.color" variant="subtle" size="lg">
            {{ statusBadge.label }}
          </UBadge>
          <UBadge :color="difficultyBadge.color" variant="subtle" size="lg">
            {{ difficultyBadge.label }}
          </UBadge>
        </div>
      </div>

      <!-- Описание -->
      <div class="space-y-2">
        <h4 class="text-xl font-semibold text-highlighted">Описание</h4>
        <p class="text-base text-muted leading-relaxed">
          {{ course.short_description }}
        </p>
      </div>

      <!-- Информация о курсе -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Преподаватель -->
        <div
          class="flex items-center gap-3 p-4 rounded-lg bg-elevated border border-default"
        >
          <UIcon name="i-heroicons-user" class="size-8 text-primary" />
          <div>
            <p class="text-sm text-muted">Преподаватель</p>
            <p class="text-lg font-semibold text-highlighted">
              {{ course.teacher_name }}
            </p>
          </div>
        </div>

        <!-- Категория -->
        <div
          class="flex items-center gap-3 p-4 rounded-lg bg-elevated border border-default"
        >
          <UIcon name="i-heroicons-tag" class="size-8 text-primary" />
          <div>
            <p class="text-sm text-muted">Категория</p>
            <p class="text-lg font-semibold text-highlighted">
              {{ course.category_name }}
            </p>
          </div>
        </div>

        <!-- Длительность -->
        <div
          v-if="course.duration_weeks"
          class="flex items-center gap-3 p-4 rounded-lg bg-elevated border border-default"
        >
          <UIcon name="i-heroicons-clock" class="size-8 text-primary" />
          <div>
            <p class="text-sm text-muted">Длительность</p>
            <p class="text-lg font-semibold text-highlighted">
              {{ course.duration_weeks }} недель
            </p>
          </div>
        </div>

        <!-- Количество студентов -->
        <div
          class="flex items-center gap-3 p-4 rounded-lg bg-elevated border border-default"
        >
          <UIcon name="i-heroicons-user-group" class="size-8 text-primary" />
          <div>
            <p class="text-sm text-muted">Записано студентов</p>
            <p class="text-lg font-semibold text-highlighted">
              {{ course.enrolled_count }}
              <span v-if="course.max_students" class="text-sm text-muted">
                / {{ course.max_students }}
              </span>
            </p>
          </div>
        </div>

        <!-- Дата создания -->
        <div
          class="flex items-center gap-3 p-4 rounded-lg bg-elevated border border-default"
        >
          <UIcon name="i-heroicons-calendar" class="size-8 text-primary" />
          <div>
            <p class="text-sm text-muted">Дата создания</p>
            <p class="text-base font-semibold text-highlighted">
              {{ formattedDate }}
            </p>
          </div>
        </div>

        <!-- Дата обновления -->
        <div
          class="flex items-center gap-3 p-4 rounded-lg bg-elevated border border-default"
        >
          <UIcon
            name="i-heroicons-arrow-path"
            class="size-8 text-primary"
          />
          <div>
            <p class="text-sm text-muted">Последнее обновление</p>
            <p class="text-base font-semibold text-highlighted">
              {{ updatedDate }}
            </p>
          </div>
        </div>
      </div>

      <!-- Дополнительная информация -->
      <div
        v-if="course.is_featured"
        class="flex items-center gap-2 p-4 rounded-lg bg-primary/10 border border-primary/20"
      >
        <UIcon name="i-heroicons-star" class="size-6 text-primary" />
        <p class="text-base font-semibold text-primary">
          Рекомендуемый курс
        </p>
      </div>
    </template>

    <template #footer="{ close }">
      <UButton
        label="Закрыть"
        color="neutral"
        variant="outline"
        size="lg"
        @click="close"
      />
      <div class="flex gap-3">
        <UButton
          :to="`/courses/${course.slug}`"
          label="Перейти к курсу"
          color="primary"
          size="lg"
          icon="i-heroicons-arrow-right"
          trailing
        />
      </div>
    </template>
  </UModal>
</template>
