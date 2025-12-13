<script setup lang="ts">
import type { Course } from "~/types";

interface Props {
  courses: Course[];
  pending?: boolean;
  maxItems?: number;
}

withDefaults(defineProps<Props>(), {
  pending: false,
  maxItems: 5,
});
</script>

<template>
  <UCard class="shadow-sm">
    <div
      class="px-3.5 py-2 border-b mb-2 border-default flex items-center justify-between"
    >
      <h2 class="text-2xl font-semibold text-default">Мои курсы</h2>
      <UButton
        to="/teacher/courses/create"
        icon="i-lucide-plus"
        color="primary"
        size="sm"
        variant="ghost"
      />
    </div>

    <!-- Loading -->
    <div v-if="pending" class="p-6 space-y-4">
      <USkeleton v-for="i in 3" :key="i" class="h-20 rounded-lg" />
    </div>

    <!-- Empty -->
    <div v-else-if="courses.length === 0" class="p-12 text-center">
      <UIcon name="i-lucide-book-x" class="size-12 text-muted mx-auto mb-3" />
      <p class="text-muted mb-4">У вас пока нет курсов</p>
      <UButton to="/teacher/courses/create" color="primary" size="sm">
        Создать курс
      </UButton>
    </div>

    <!-- List -->
    <div v-else class="space-y-1">
      <TeacherCoursesMyListCard
        v-for="course in courses.slice(0, maxItems)"
        :key="course.id"
        :course="course"
      />
      <UButton
        label="Все мои курсы"
        variant="soft"
        color="neutral"
        to="/teacher/courses"
        icon="i-lucide-chevron-right"
        trailing
        block
        size="lg"
        class="mt-1"
      />
    </div>
  </UCard>
</template>
