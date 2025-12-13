<script setup lang="ts">
import type { CourseDetail } from "~/types";

defineProps<{
  course: CourseDetail;
  slug: string;
}>();

const statusConfig = computed(() => ({
  published: { label: "Опубликован", color: "success" as const },
  draft: { label: "Черновик", color: "warning" as const },
  archived: { label: "Архив", color: "neutral" as const },
}));
</script>

<template>
  <UCard>
    <div class="flex items-start justify-between gap-6">
      <div>
        <NuxtLink
          to="/teacher/courses"
          class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors mb-4"
        >
          <UIcon name="i-lucide-arrow-left" class="size-4" />
          Назад к курсам
        </NuxtLink>
        <div class="flex items-center gap-3 mb-2">
          <h1 class="text-2xl font-bold text-default">{{ course.title }}</h1>
          <UBadge
            :color="statusConfig[course.status as keyof typeof statusConfig]?.color ?? 'neutral'"
          >
            {{
              statusConfig[course.status as keyof typeof statusConfig]?.label ??
              course.status
            }}
          </UBadge>
        </div>
        <p class="text-muted">{{ course.short_description }}</p>
      </div>

      <div class="flex items-center gap-2">
        <UButton
          :to="`/teacher/courses/${slug}/edit`"
          icon="i-lucide-pencil"
          color="neutral"
          variant="soft"
        >
          Редактировать
        </UButton>
        <UButton
          :to="`/courses/${slug}`"
          icon="i-lucide-external-link"
          color="neutral"
          variant="ghost"
        >
          Просмотр
        </UButton>
      </div>
    </div>
  </UCard>
</template>
