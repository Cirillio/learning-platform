<script setup lang="ts">
import type { Course } from "~/types";

defineProps<{
  courses: Course[];
  pending: boolean;
}>();
</script>

<template>
  <div class="space-y-4">
    <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Мои курсы</h2>
    <div v-if="pending" class="py-4">
      <USkeleton class="h-32 w-full" />
    </div>
    <div v-else-if="courses.length > 0">
      <CoursesCatalogCardGrid :courses="courses">
        <CoursesCatalogCard
          v-for="course in courses"
          :key="course.id"
          :course="course"
          :can-enroll="false"
          :pending="false"
          :enrolled="true"
        />
      </CoursesCatalogCardGrid>
    </div>
    <UAlert
      v-else
      title="Нет активных курсов"
      description="Вы еще не записались ни на один курс."
      color="neutral"
      variant="subtle"
      :actions="[
        {
          label: 'Каталог курсов',
          to: '/courses',
          variant: 'solid',
          color: 'primary',
        },
      ]"
    />
  </div>
</template>
