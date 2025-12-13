<script setup lang="ts">
import type { Course } from "~/types";

defineProps<{
  courses: Course[];
}>();
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
    <UCard v-for="course in courses" :key="course.id">
      <!-- Cover Image -->
      <div
        class="aspect-video bg-muted/25 ring ring-default rounded-md relative overflow-hidden"
      >
        <img
          v-if="course.cover_image_url"
          :src="course.cover_image_url"
          :alt="course.title"
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <div v-else class="w-full h-full flex items-center justify-center">
          <UIcon name="i-lucide-image" class="size-12 text-muted" />
        </div>

        <!-- Status Badge -->
        <UBadge
          :color="
            course.status === 'published'
              ? 'success'
              : course.status === 'draft'
              ? 'warning'
              : 'neutral'
          "
          size="lg"
          class="absolute top-3 right-3"
        >
          {{
            course.status === "published"
              ? "Опубликован"
              : course.status === "draft"
              ? "Черновик"
              : "Архив"
          }}
        </UBadge>
      </div>

      <!-- Content -->
      <div>
        <h3 class="font-semibold text-2xl text-default mb-1 mt-3 line-clamp-1">
          {{ course.title }}
        </h3>
        <p class="text-lg text-muted line-clamp-2 mb-3">
          {{ course.short_description }}
        </p>

        <!-- Stats -->
        <div class="flex items-center gap-4 text-base text-muted mb-4">
          <span class="flex items-center gap-1">
            <UIcon name="i-lucide-users" class="size-5" />
            {{ course.enrolled_count }} студентов
          </span>
          <span class="flex items-center gap-1">
            <UIcon name="i-lucide-book-open" class="size-5" />
            {{
              course.difficulty === "beginner"
                ? "Начальный"
                : course.difficulty === "intermediate"
                ? "Средний"
                : "Продвинутый"
            }}
          </span>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-2">
          <UButton
            :to="`/teacher/courses/${course.slug}`"
            color="secondary"
            block
            class="flex-1 text-base"
          >
            Управление
          </UButton>
          <UButton
            :to="`/teacher/courses/${course.slug}/edit`"
            icon="i-lucide-pencil"
            color="neutral"
            variant="ghost"
            size="lg"
          />
          <UButton
            :to="`/courses/${course.slug}`"
            icon="i-lucide-external-link"
            color="neutral"
            variant="ghost"
            size="lg"
          />
        </div>
      </div>
    </UCard>
  </div>
</template>
