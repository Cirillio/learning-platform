<script setup lang="ts">
import type { Lesson } from "~/types";

defineProps<{
  lessons: Lesson[];
  loading: boolean;
  slug: string;
}>();

const emit = defineEmits<{
  (e: "add"): void;
  (e: "delete", lessonId: number): void;
}>();
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-semibold text-default">Уроки курса</h2>
        <UButton
          icon="i-lucide-plus"
          color="primary"
          size="lg"
          @click="emit('add')"
        >
          Добавить урок
        </UButton>
      </div>
    </template>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3">
      <USkeleton v-for="i in 4" :key="i" class="h-20 rounded-xl" />
    </div>

    <!-- Empty -->
    <div v-else-if="lessons.length === 0" class="text-center py-8">
      <UIcon name="i-lucide-book-x" class="size-12 text-muted mx-auto mb-3" />
      <p class="text-muted mb-4">Уроков пока нет</p>
      <UButton icon="i-lucide-plus" color="primary" @click="emit('add')">
        Добавить первый урок
      </UButton>
    </div>

    <!-- List -->
    <div v-else class="space-y-3">
      <TeacherCoursesDetailListItem
        v-for="lesson in lessons"
        :key="lesson.id"
        :desc="lesson.description"
        :order="lesson.order"
        :subdesc="lesson.duration_minutes + ' мин.'"
        :link="'/teacher/courses/' + slug + '/lessons/' + lesson.slug"
        @delete="() => emit('delete', lesson.id)"
      >
        <template #leading>
          <div
            class="size-12 rounded-lg opacity-50 group-hover:opacity-100 transition-all bg-primary/10 flex items-center justify-center text-2xl font-semibold text-primary shrink-0"
          >
            {{ lesson.order }}
          </div>
        </template>

        <template #title>
          <NuxtLink
            :to="`/teacher/courses/${slug}/lessons/${lesson.slug}`"
            class="font-medium text-xl text-default"
            >{{ lesson.title }}</NuxtLink
          >
          <UBadge
            v-if="!lesson.is_published"
            color="warning"
            variant="soft"
            size="sm"
          >
            Черновик
          </UBadge>
        </template>
      </TeacherCoursesDetailListItem>
    </div>
  </UCard>
</template>
