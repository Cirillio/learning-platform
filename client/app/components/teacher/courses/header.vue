<script setup lang="ts">
defineProps<{
  statusFilter: string;
}>();

const emit = defineEmits<{
  (e: "update:statusFilter", value: string): void;
}>();

const statusOptions = [
  { label: "Все", value: "all" },
  { label: "Опубликованы", value: "published" },
  { label: "Черновики", value: "draft" },
  { label: "Архив", value: "archived" },
];
</script>

<template>
  <div class="flex flex-col gap-2 pb-3 items-start justify-between">
    <p class="text-3xl font-semibold">
      Управляйте своими курсами и учебными материалами
    </p>

    <UButton
      to="/teacher/courses/create"
      icon="i-lucide-plus"
      color="primary"
      size="lg"
    >
      Создать курс
    </UButton>

    <!-- Filters -->
    <UTabs
      :items="statusOptions.map((s) => ({ label: s.label, value: s.value }))"
      :model-value="statusFilter"
      @update:model-value="emit('update:statusFilter', $event as string)"
      class="w-fit -mb-2"
    />
  </div>
</template>
