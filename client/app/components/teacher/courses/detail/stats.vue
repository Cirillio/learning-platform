<script setup lang="ts">
import type { CourseDetail } from "~/types";

defineProps<{
  course: CourseDetail;
}>();

const stats = computed(() => [
  {
    icon: "i-lucide-users",
    iconColor: "text-primary",
    bgColor: "bg-primary/10",
    value: (val: CourseDetail) => val.enrolled_count,
    label: "Студентов",
  },
  {
    icon: "i-lucide-book-open",
    iconColor: "text-success",
    bgColor: "bg-success/10",
    value: (val: CourseDetail) => val.lessons_count,
    label: "Уроков",
  },
  {
    icon: "i-lucide-clipboard-list",
    iconColor: "text-warning",
    bgColor: "bg-warning/10",
    value: (val: CourseDetail) => val.assignments_count,
    label: "Заданий",
  },
  {
    icon: "i-lucide-clock",
    iconColor: "text-info",
    bgColor: "bg-info/10",
    value: (val: CourseDetail) => val.duration_weeks || "—",
    label: "Недель",
  },
]);
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-4 gap-2">
    <TeacherDashboardStatCard
      v-for="stat in stats"
      :key="stat.label"
      :stat="{ ...stat, value: stat.value(course) }"
    />
  </div>
</template>
