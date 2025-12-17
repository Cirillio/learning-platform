<script setup lang="ts">
const props = defineProps<{
  open: boolean;
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (
    e: "submit",
    lesson: {
      title: string;
      description: string;
      slug: string;
      duration_minutes: number;
    }
  ): void;
}>();

const form = reactive({
  title: "",
  description: "",
  slug: "",
  duration_minutes: 30,
});

const isSubmitting = ref(false);

const handleSubmit = () => {
  if (!form.title) return;
  emit("submit", { ...form });
  form.title = "";
  form.description = "";
  form.slug = "";
  form.duration_minutes = 30;
};

const closeModal = () => emit("update:open", false);

// Expose for parent to control loading state
defineExpose({
  setLoading: (loading: boolean) => {
    isSubmitting.value = loading;
  },
});
</script>

<template>
  <UModal :open="open" @update:open="emit('update:open', $event)">
    <template #content>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-default mb-6">Добавить урок</h3>

        <form class="space-y-4" @submit.prevent="handleSubmit">
          <UFormField label="Название урока" required>
            <UInput
              v-model="form.title"
              placeholder="Введение в курс"
              class="w-full"
            />
          </UFormField>

          <UFormField label="Slug" description="URL имя урока">
            <UInput
              v-model="form.slug"
              placeholder="vvedenie-v-kurs"
              class="w-full"
            />
          </UFormField>

          <UFormField label="Описание">
            <UTextarea
              v-model="form.description"
              placeholder="Краткое описание урока"
              :rows="3"
              class="w-full"
            />
          </UFormField>

          <UFormField label="Длительность (мин)">
            <UInput
              v-model.number="form.duration_minutes"
              type="number"
              :min="1"
              :max="300"
              class="w-full"
            />
          </UFormField>

          <div class="flex justify-end gap-3 pt-4">
            <UButton
              type="button"
              color="neutral"
              variant="ghost"
              @click="closeModal"
            >
              Отмена
            </UButton>
            <UButton type="submit" color="primary" :loading="isSubmitting">
              Добавить
            </UButton>
          </div>
        </form>
      </div>
    </template>
  </UModal>
</template>
