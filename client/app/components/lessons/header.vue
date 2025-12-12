<script setup lang="ts">
import type { LessonDetail } from "~/types";
import type { BreadcrumbItem } from "@nuxt/ui";

interface Props {
  lesson: LessonDetail;
  breadcrumbs: BreadcrumbItem[];
  progressPercent: number;
  isCompleted: boolean;
}

const props = defineProps<Props>();
</script>

<template>
  <UCard
    class="dark:bg-muted/25 bg-muted/75 shadow-xs rounded-none ring-0 my-2 border-y border-default"
  >
    <LayoutContainer class="py-6">
      <!-- Breadcrumbs -->
      <UBreadcrumb :items="breadcrumbs" class="mb-4" />

      <div
        class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4"
      >
        <!-- Title & Meta -->
        <div class="space-y-2">
          <div class="flex items-center gap-3">
            <h1 class="text-2xl lg:text-3xl font-bold text-default">
              {{ lesson.title }}
            </h1>
            <UBadge
              v-if="isCompleted"
              color="success"
              variant="soft"
              icon="i-lucide-check-circle"
              label="Завершён"
            />
          </div>

          <div class="flex items-center gap-4 text-sm text-muted">
            <span class="flex items-center gap-1.5">
              <UIcon name="i-lucide-clock" class="size-4" />
              {{ lesson.duration_minutes || "—" }} мин
            </span>
            <span class="flex items-center gap-1.5">
              <UIcon name="i-lucide-file-text" class="size-4" />
              {{ lesson.materials.length }} материалов
            </span>
            <span
              v-if="lesson.assignments_count"
              class="flex items-center gap-1.5"
            >
              <UIcon name="i-lucide-clipboard-list" class="size-4" />
              {{ lesson.assignments_count }} заданий
            </span>
          </div>
        </div>
      </div>
    </LayoutContainer>
  </UCard>
</template>
