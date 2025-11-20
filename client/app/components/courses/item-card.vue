<!-- components/courses/item-card.vue -->
<script lang="ts" setup>
import type { Course } from "~/types";

interface Props {
  course: Course;
  canEnroll?: boolean;
  enrolled?: boolean;
  pending?: boolean;
  onEnroll?: () => void;
}

const props = withDefaults(defineProps<Props>(), {
  canEnroll: false,
  enrolled: false,
  pending: false,
});

const difficultyBadge = computed(() => {
  const badges = {
    beginner: { label: "Начальный", color: "success" as const },
    intermediate: { label: "Средний", color: "warning" as const },
    advanced: { label: "Продвинутый", color: "accent" as const },
  };
  return badges[props.course.difficulty] || badges.beginner;
});

const statusBadge = computed(() => {
  const statuses = {
    draft: { label: "Черновик", color: "neutral" as const },
    published: { label: "Опубликован", color: "success" as const },
    archived: { label: "Архив", color: "neutral" as const },
  };
  return statuses[props.course.status] || statuses.draft;
});

const isModalOpen = ref(false);
</script>

<template>
  <UCard
    :ui="{
      body: 'flex flex-col',
    }"
  >
    <div class="space-y-1">
      <!-- Бейджи -->
      <div class="flex gap-2">
        <NuxtLink class="mr-auto" :to="'/courses/categories/' + course.category">
          <UBadge color="info" variant="subtle" size="lg">
            {{ course.category_name }}
          </UBadge>
        </NuxtLink>
        <UBadge :color="statusBadge.color" variant="subtle" size="lg">
          {{ statusBadge.label }}
        </UBadge>
        <UBadge :color="difficultyBadge.color" variant="subtle" size="lg">
          {{ difficultyBadge.label }}
        </UBadge>
      </div>

      <!-- Заголовок -->
      <NuxtLink :to="`/courses/${course.slug}`" class="block mt-2">
        <h3
          class="text-3xl font-bold text-default hover:text-primary transition-colors line-clamp-2"
        >
          {{ course.title }}
        </h3>
      </NuxtLink>

      <!-- Описание -->
      <p class="text-lg text-muted line-clamp-2">
        {{ course.short_description }}
      </p>
    </div>

    <div class="flex items-center mt-auto gap-4 justify-between">
      <!-- Преподаватель -->
      <div class="flex items-center mt-auto gap-2 border-t border-default">
        <span class="font-light">Преподаватель:</span>
        <span class="text-base text-secondary font-semibold">
          {{ course.teacher_name || "Преподаватель не указан или ещё не назначен" }}
        </span>
      </div>

      <!-- 🆕 Кнопки с учётом pending -->
      <div class="flex gap-4 justify-end">
        <!-- Показываем скелетон пока грузятся данные о записи -->
        <USkeleton v-if="pending && canEnroll" class="h-9 w-24 bg-primary" />

        <!-- Записаться -->
        <UButton
          v-else-if="canEnroll && !enrolled"
          :to="`/courses/${course.slug}/enroll`"
          label="Записаться"
          color="primary"
          size="lg"
          @click="onEnroll"
        />

        <!-- Перейти к курсу -->
        <UButton
          v-else-if="enrolled"
          :to="`/courses/${course.slug}`"
          label="Перейти к курсу"
          color="success"
          size="lg"
        />

        <!-- Подробнее (гости/препы) -->
        <UButton
          v-else
          label="Подробнее"
          color="secondary"
          size="lg"
          @click="isModalOpen = true"
        />
      </div>
    </div>
  </UCard>

  <CoursesItemDetailsModal v-model:open="isModalOpen" :course="course" />
</template>
