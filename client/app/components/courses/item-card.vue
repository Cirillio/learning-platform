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
    beginner: {
      label: "Начальный",
      color: "primary" as const,
      icon: "i-heroicons-arrow-trending-up",
    },
    intermediate: {
      label: "Средний",
      color: "warning" as const,
      icon: "i-heroicons-minus",
    },
    advanced: {
      label: "Продвинутый",
      color: "error" as const,
      icon: "i-heroicons-bolt",
    },
  };
  return badges[props.course.difficulty] || badges.beginner;
});

const itemImageUrl = computed(() => {
  return (
    props.course.cover_image_url ||
    "https://itf-russia.ru/wp-content/uploads/2016/03/placeholder.jpg"
  );
});
</script>

<template>
  <UCard
    :ui="{
      root: 'bg-muted dark:bg-muted/25 hover:ring-primary/25 shadow-xs hover:shadow-md transition-shadow duration-200 ease-in-out group ',
      header: '!p-0 border-0',
      body: 'border-0 !p-3',
    }"
  >
    <template #header>
      <div class="aspect-video overflow-hidden relative">
        <NuxtImg
          :src="itemImageUrl"
          class="object-cover object-center z-0 w-full h-full transition-transform duration-300 ease-in-out"
        />
        <UBadge
          v-if="course.status === 'draft'"
          color="info"
          variant="subtle"
          size="sm"
          class="absolute top-2 right-6 z-10"
          label="Черновик"
        />
        <UBadge
          v-if="course.status === 'archived'"
          color="warning"
          variant="subtle"
          size="lg"
          class="absolute top-2 right-6 z-10"
          label="В архиве"
        />

        <UBadge
          v-if="enrolled"
          class="absolute bottom-2 left-6 z-10"
          label="Вы записаны"
          color="success"
          variant="subtle"
        />
      </div>
    </template>

    <div class="flex flex-col gap-1">
      <div class="flex flex-col gap-1 items-start">
        <UBadge
          :label="difficultyBadge.label"
          :color="difficultyBadge.color"
          :icon="difficultyBadge.icon"
          size="md"
          variant="subtle"
        />
        <NuxtLink :to="'/courses/' + course.slug">
          <UBadge
            :label="course.category_name"
            variant="outline"
            color="neutral"
            size="md"
            class="hover:opacity-75 transition-opacity duration-150"
          />
        </NuxtLink>
      </div>

      <NuxtLink :to="`/courses/${course.slug}`" class="block w-fit mt-1">
        <h3
          class="text-2xl font-bold text-gray-900 dark:text-white group-hover:text-primary transition-colors duration-200 line-clamp-1 truncate"
        >
          {{ course.title }}
        </h3>
      </NuxtLink>
      <p
        class="text-base text-gray-500 dark:text-gray-400 line-clamp-1 truncate"
      >
        {{ course.short_description }}
      </p>

      <div class="mt-2 flex flex-col gap-2">
        <div class="flex gap-2 text-muted items-center">
          <UIcon name="heroicons:clock" class="size-5" />
          <span class="text-sm">Длительность:</span>
          <UBadge
            :label="course.duration_weeks + ' нед.'"
            variant="outline"
            color="neutral"
            size="md"
          />
        </div>
        <div class="flex gap-2 text-muted items-center">
          <UIcon name="heroicons:user-group" class="size-5" />
          <span class="text-sm">Участников:</span>
          <UBadge
            :label="course.enrolled_count + ' чел.'"
            variant="outline"
            color="neutral"
            size="md"
          />
        </div>
      </div>

      <span class="mt-4 font-semibold text-xs text-dimmed">
        Автор:

        <NuxtLink :to="'/teachers/' + course.teacher">
          {{ course.teacher_name || "N/A" }}
        </NuxtLink>
      </span>
    </div>
  </UCard>
</template>
