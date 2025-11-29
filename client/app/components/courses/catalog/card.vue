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
      label: "Junior",
      color: "primary" as const,
      icon: "i-heroicons-arrow-trending-up",
    },
    intermediate: {
      label: "Middle",
      color: "warning" as const,
      icon: "i-heroicons-minus",
    },
    advanced: {
      label: "Senior",
      color: "error" as const,
      icon: "i-heroicons-bolt",
    },
  };
  return badges[props.course.difficulty] || badges.beginner;
});
</script>

<template>
  <UCard
    :ui="{
      root: 'flex flex-col bg-muted ring-muted dark:bg-muted/25 hover:ring-primary/50 shadow-xs hover:shadow-md transition-shadow duration-200 ease-in-out group ',
      header: '!p-0 border-0',
      body: 'border-0 py-1! px-2! sm:py-2! sm:px-3! flex h-full w-full',
    }"
  >
    <template #header>
      <div class="aspect-video overflow-hidden relative">
        <NuxtImg
          v-if="props.course.cover_image_url"
          :src="props.course.cover_image_url"
          class="object-cover object-center z-0 w-full h-full transition-transform duration-300 ease-in-out"
        />
        <picture
          class="flex bg-linear-to-t from-primary/75 items-end to-success/75 w-full h-full"
        >
          <span
            class="font-extrabold text-2xl sm:text-4xl lg:text-6xl py-3! px-2! sm:py-4! sm:px-3! line-clamp-2 overflow-hidden text-balance h-fit text-white/25 dark:text-default/50"
          >
            {{ course.abbr }}
          </span>
        </picture>
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
        <div
          v-if="enrolled"
          class="absolute flex bottom-0 left-1/2 overflow-hidden -translate-x-1/2 border rounded-t-md border-default bg-default"
        >
          <span
            class="px-3 py-1 font-medium text-sm bg-muted/75 dark:bg-muted/25 text-primary"
          >
            Вы записаны
          </span>
        </div>
      </div>
    </template>

    <div class="flex flex-col w-full gap-1">
      <NuxtLink
        :to="`/courses/${course.slug}`"
        class="flex items-center justify-between w-full text-default hover:text-primary transition-colors duration-200 group/title"
      >
        <h3
          class="text-sm sm:text-lg xl:text-2xl font-bold transition-colors duration-200 h-fit line-clamp-2 overflow-hidden"
        >
          {{ course.title }}
        </h3>
        <UIcon
          name="heroicons:arrow-right"
          class="size-5 opacity-25 group-hover/title:opacity-100 transition-opacity duration-200"
        />
      </NuxtLink>
      <p
        class="text-xs text-balance md:text-base text-gray-500 dark:text-gray-400 line-clamp-2 overflow-hidden"
      >
        {{ course.short_description }}
      </p>

      <USeparator class="sm:hidden mt-auto" />

      <div class="flex justify-between mt-auto gap-2">
        <ul class="flex gap-2 text-sm text-muted">
          <li>
            <span class="font-extrabold">·</span>
            {{ course.duration_weeks }} нед.
          </li>
          <li>
            <span class="font-extrabold">·</span>
            {{ course.enrolled_count }} чел.
          </li>
        </ul>
        <div class="flex gap-1 text-sm text-muted">
          <span class="font-extrabold">·</span>
          <span :class="['text-' + difficultyBadge.color]">
            {{ difficultyBadge.label }}
          </span>
        </div>
      </div>
    </div>
  </UCard>
</template>
