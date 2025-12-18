<script setup lang="ts">
definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Задания курса",
});

const route = useRoute();
const courseSlug = computed(() => route.params.slug as string);
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          Задания курса
        </h1>
        <p class="text-gray-500 dark:text-gray-400">
          Управление заданиями и проверкой
        </p>
      </div>
      <UButton
        :to="`/teacher/courses/${courseSlug}/assignments/create`"
        icon="i-lucide-plus"
        color="primary"
      >
        Создать задание
      </UButton>
    </div>

    <TeacherAssignmentsList :course-slug="courseSlug" />
  </div>
</template>
