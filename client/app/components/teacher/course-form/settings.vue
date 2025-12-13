<script setup lang="ts">
defineProps<{
  form: {
    category: number;
    difficulty: string;
    duration_weeks: number | null;
    max_students: number | null;
  };
  categoryOptions: { label: string; value: number }[];
  difficultyOptions: { label: string; value: string }[];
}>();
</script>

<template>
  <UCard>
    <template #header>
      <h2 class="text-lg font-semibold text-default">Настройки</h2>
    </template>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Category -->
      <UFormField label="Категория" required>
        <USelect
          v-model="form.category"
          :items="categoryOptions"
          placeholder="Выберите категорию"
          class="w-full"
        />
      </UFormField>

      <!-- Difficulty -->
      <UFormField label="Уровень сложности" required>
        <USelect
          v-model="form.difficulty"
          :items="difficultyOptions"
          class="w-full"
        />
      </UFormField>

      <!-- Duration -->
      <UFormField
        label="Длительность (недель)"
        hint="Оставьте пустым, если не определено"
      >
        <UInput
          v-model.number="form.duration_weeks"
          type="number"
          :min="1"
          :max="52"
          placeholder="Например: 8"
          class="w-full"
        />
      </UFormField>

      <!-- Max Students -->
      <UFormField
        label="Максимум студентов"
        hint="Оставьте пустым для неограниченного"
      >
        <UInput
          v-model.number="form.max_students"
          type="number"
          :min="1"
          :max="1000"
          placeholder="Например: 100"
          class="w-full"
        />
      </UFormField>
    </div>
  </UCard>
</template>
