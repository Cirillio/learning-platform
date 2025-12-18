<script setup lang="ts">
definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Уроки курса",
});

const route = useRoute();
const courseSlug = computed(() => route.params.slug as string);
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          Уроки курса
        </h1>
        <p class="text-gray-500 dark:text-gray-400">
          Управление уроками и материалами
        </p>
      </div>
      <UButton
        :to="`/teacher/courses/${courseSlug}/lessons/create`"
        icon="i-lucide-plus"
        color="primary"
      >
        Создать урок
      </UButton>
    </div>

    <TeacherLessonsList :course-slug="courseSlug" />
  </div>
</template>
