<script setup lang="ts">
defineProps<{
  form: {
    title: string;
    short_description: string;
    description: string;
  };
}>();
</script>

<template>
  <UCard>
    <template #header>
      <h2 class="text-lg font-semibold text-default">Основная информация</h2>
    </template>

    <div class="space-y-6">
      <!-- Title -->
      <UFormField label="Название курса" required>
        <UInput
          v-model="form.title"
          placeholder="Например: Основы веб-разработки"
          class="w-full"
        />
      </UFormField>

      <!-- Short Description -->
      <UFormField
        label="Краткое описание"
        required
        hint="Будет показано в карточке курса"
      >
        <UTextarea
          v-model="form.short_description"
          placeholder="Краткое описание курса в 1-2 предложения"
          :rows="2"
          class="w-full"
        />
      </UFormField>

      <!-- Description -->
      <UFormField
        label="Полное описание"
        required
        hint="Поддерживается Markdown"
      >
        <UTextarea
          v-model="form.description"
          placeholder="Подробное описание курса, программа обучения, что студент получит..."
          :rows="8"
          class="w-full"
        />
      </UFormField>
    </div>
  </UCard>
</template>
