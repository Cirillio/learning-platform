<script setup lang="ts">
import type { Lesson } from "~/types";

interface Props {
  open: boolean;
  lesson: Lesson | null;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (
    e: "submit",
    data: {
      title: string;
      description: string;
      duration_minutes: number;
      is_published: boolean;
    }
  ): void;
}>();

const form = reactive({
  title: "",
  description: "",
  duration_minutes: 30,
  is_published: false,
});

const isSubmitting = ref(false);

// Синхронизация формы при открытии с данными урока
watch(
  () => props.lesson,
  (lesson) => {
    if (lesson) {
      form.title = lesson.title;
      form.description = lesson.description || "";
      form.duration_minutes = lesson.duration_minutes;
      form.is_published = lesson.is_published;
    }
  },
  { immediate: true }
);

const handleSubmit = () => {
  if (!form.title.trim()) return;
  emit("submit", { ...form });
};

const closeModal = () => emit("update:open", false);

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
        <h3 class="text-xl font-semibold text-default mb-6">
          Редактировать урок
        </h3>

        <form class="space-y-4" @submit.prevent="handleSubmit">
          <UFormField label="Название урока" required size="lg">
            <UInput
              v-model="form.title"
              placeholder="Введение в курс"
              class="w-full"
              size="lg"
            />
          </UFormField>

          <UFormField label="Описание" size="lg">
            <UTextarea
              v-model="form.description"
              placeholder="Краткое описание урока"
              :rows="3"
              class="w-full"
              size="lg"
            />
          </UFormField>

          <UFormField label="Длительность (мин)" size="lg">
            <UInput
              v-model.number="form.duration_minutes"
              type="number"
              :min="1"
              :max="300"
              class="w-full"
              size="lg"
            />
          </UFormField>

          <UCheckbox
            v-model="form.is_published"
            label="Опубликовать урок"
            description="Студенты смогут видеть этот урок"
          />

          <div class="flex justify-end gap-3 pt-4">
            <UButton
              type="button"
              color="neutral"
              variant="ghost"
              size="lg"
              @click="closeModal"
            >
              Отмена
            </UButton>
            <UButton
              type="submit"
              color="primary"
              size="lg"
              :loading="isSubmitting"
            >
              Сохранить
            </UButton>
          </div>
        </form>
      </div>
    </template>
  </UModal>
</template>
