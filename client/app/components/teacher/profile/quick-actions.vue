<script setup lang="ts">
// Quick actions for teacher profile
const quickActions = ref([
  {
    label: "Создать новый курс",
    to: "/teacher/courses/create",
    icon: "i-lucide-plus",
    color: "primary" as const,
    block: true,
  },
  {
    label: "Управление курсами",
    to: "/teacher/courses",
    icon: "i-lucide-book-open",
    color: "neutral" as const,
    variant: "soft" as const,
    block: true,
  },
  {
    label: "Проверить работы",
    to: "/teacher/grading",
    icon: "i-lucide-clipboard-check",
    color: "warning" as const,
    variant: "soft" as const,
    block: true,
  },
  {
    label: "Мои студенты",
    to: "/teacher/students",
    icon: "i-lucide-users",
    color: "info" as const,
    variant: "soft" as const,
    block: true,
  },
]);
</script>

<template>
  <UCard>
    <template #header>
      <h2 class="text-2xl font-semibold text-default">Быстрые действия</h2>
    </template>

    <div class="gap-2 flex">
      <UButton
        v-for="action in quickActions"
        :key="action.to"
        size="xl"
        v-bind="action"
      />
    </div>
  </UCard>
</template>
