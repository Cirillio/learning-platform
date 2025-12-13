<script setup lang="ts">
withDefaults(
  defineProps<{
    statusFilter?: string;
    onUpdate?: () => void;
  }>(),
  {
    statusFilter: "all",
    onUpdate: () => {},
  }
);
</script>

<template>
  <div class="text-center py-20">
    <UIcon name="i-lucide-book-x" class="size-16 text-muted mx-auto mb-4" />
    <h2 class="text-xl font-semibold text-default mb-2">
      {{
        statusFilter === "all" ? "У вас пока нет курсов" : "Курсы не найдены"
      }}
    </h2>
    <p class="text-muted mb-6">
      {{
        statusFilter === "all"
          ? "Создайте свой первый курс и начните обучать студентов"
          : "Нет курсов с выбранным статусом"
      }}
    </p>

    <UButton
      v-if="statusFilter === 'all'"
      to="/teacher/courses/create"
      icon="i-lucide-plus"
      color="primary"
    >
      Создать курс
    </UButton>
    <UButton
      v-if="statusFilter === 'all'"
      icon="i-lucide-refresh-ccw"
      color="primary"
      class="ml-3"
      @click="onUpdate"
    >
      Обновить
    </UButton>
  </div>
</template>
