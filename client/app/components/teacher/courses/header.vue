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

    <div class="flex items-center justify-between w-full gap-2">
      <!-- Filters -->
      <UTabs
        :items="statusOptions.map((s) => ({ label: s.label, value: s.value }))"
        :model-value="statusFilter"
        @update:model-value="emit('update:statusFilter', $event as string)"
        class="w-fit"
        variant="link"
        :ui="{
          content: 'hidden',
          label: 'cursor-pointer text-lg',
        }"
      />

      <UButton
        to="/teacher/courses/create"
        icon="i-lucide-plus"
        color="primary"
        size="lg"
      >
        Создать курс
      </UButton>
    </div>
  </div>
</template>
