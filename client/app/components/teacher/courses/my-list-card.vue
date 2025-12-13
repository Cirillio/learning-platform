<script lang="ts" setup>
import type { Course, CourseDetail } from "~/types";

interface Props {
  course: Course | CourseDetail;
  showThumb?: boolean;
}

withDefaults(defineProps<Props>(), {
  showThumb: false,
});

const getStatusColor = (status: string) => {
  const colors: Record<string, "success" | "warning" | "neutral"> = {
    published: "success",
    draft: "warning",
    archived: "neutral",
  };
  return colors[status] || "neutral";
};

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    published: "Опубликован",
    draft: "Черновик",
    archived: "Архив",
  };
  return labels[status] || status;
};
</script>

<template>
  <UButton
    :to="`/teacher/courses/${course.slug}`"
    variant="soft"
    color="neutral"
    class="flex gap-2 items-start px-3.5 py-2 group relative rounded-l-none transition-colors"
  >
    <div
      class="absolute left-0 top-0 bottom-0 w-1 bg-primary/25 group-hover:bg-primary/75 transition-colors"
    ></div>

    <NuxtImg
      v-if="showThumb"
      :src="course.cover_image_url || '/images/course-placeholder.png'"
      :alt="`${course.title}`"
      class="w-16 h-16 rounded-lg object-cover ring overflow-hidden ring-muted shrink-0"
      width="64"
      height="64"
    />

    <div class="flex flex-col w-full gap-2">
      <h3 class="font-semibold text-default text-xl truncate flex-1">
        {{ course.title }}
      </h3>

      <div class="flex justify-between w-full">
        <UBadge :color="getStatusColor(course.status)" variant="soft">
          {{ getStatusLabel(course.status) }}
        </UBadge>

        <span class="flex items-center text-muted gap-1 text-sm">
          <span>Записано: </span>
          {{ course.enrolled_count }}
          <UIcon name="i-lucide-users" class="size-4" />
        </span>
      </div>
    </div>
  </UButton>
</template>
