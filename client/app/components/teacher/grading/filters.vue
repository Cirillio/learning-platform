<script setup lang="ts">
defineProps<{
  statusFilter: string;
}>();

const emit = defineEmits<{
  (e: "update:statusFilter", value: string): void;
}>();

const statusOptions = [
  { label: "На проверке", value: "pending" },
  { label: "Оценено", value: "graded" },
  { label: "Все", value: "all" },
];
</script>

<template>
  <div class="flex items-center gap-4 mb-6">
    <UTabs
      :items="statusOptions.map((s) => ({ label: s.label, value: s.value }))"
      :model-value="statusFilter"
      @update:model-value="emit('update:statusFilter', $event as string)"
      class="w-fit"
    />
  </div>
</template>
