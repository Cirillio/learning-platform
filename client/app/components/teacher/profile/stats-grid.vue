<script setup lang="ts">
interface Stats {
  totalCourses: number;
  publishedCourses: number;
  totalStudents: number;
  totalLessons: number;
}

defineProps<{
  stats: Stats;
}>();
</script>

<template>
  <div class="w-full grid grid-cols-2 grid-rows-2 gap-2">
    <TeacherProfileStatCard
      :color="'primary'"
      :icon="'i-lucide-book-open'"
      :value="stats.totalCourses"
      :label="'Курсов'"
    />

    <TeacherProfileStatCard
      :color="'success'"
      :icon="'i-lucide-check-circle'"
      :value="stats.publishedCourses"
      :label="'Опубликовано'"
    />

    <TeacherProfileStatCard
      :color="'info'"
      :icon="'i-lucide-users'"
      :value="stats.totalStudents"
      :label="'Студентов'"
    />
    <TeacherProfileStatCard
      :color="'warning'"
      :icon="'i-lucide-play-circle'"
      :value="stats.totalLessons"
      :label="'Уроков'"
    />
  </div>
</template>
