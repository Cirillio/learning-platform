<script setup lang="ts">
import type { CourseDetail } from "~/types";

defineProps<{
  courses: CourseDetail[];
  pending: boolean;
  refresh?: () => void;
}>();
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-semibold text-default">Мои курсы</h2>
        <UButton
          to="/teacher/courses/create"
          icon="i-lucide-plus"
          color="primary"
          variant="ghost"
        >
        </UButton>
      </div>
    </template>

    <div v-if="pending" class="space-y-3">
      <USkeleton v-for="i in 3" :key="i" class="h-20 rounded-xl" />
    </div>

    <TeacherCoursesEmptyState
      v-else-if="courses.length === 0"
      @update="refresh"
    />

    <div v-else class="space-y-1">
      <TeacherCoursesMyListCard
        v-for="course in courses"
        :key="course.id"
        :course="course"
        :show-thumb="true"
      />
    </div>
  </UCard>
</template>
