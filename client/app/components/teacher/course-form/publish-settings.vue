<script setup lang="ts">
defineProps<{
  form: {
    status: string;
  };
  statusOptions: { label: string; value: string }[];
}>();
</script>

<template>
  <UCard>
    <template #header>
      <h2 class="text-lg font-semibold text-default">Публикация</h2>
    </template>

    <UFormField label="Статус">
      <URadioGroup
        v-model="form.status"
        :items="statusOptions"
        class="flex gap-4"
      />
    </UFormField>

    <UAlert
      v-if="form.status === 'published'"
      color="warning"
      variant="soft"
      icon="i-lucide-alert-triangle"
      title="Внимание"
      description="Курс сразу станет доступен для записи студентов. Убедитесь, что вся информация корректна."
      class="mt-4"
    />
  </UCard>
</template>
