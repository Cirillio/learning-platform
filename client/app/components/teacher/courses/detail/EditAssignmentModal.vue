<script setup lang="ts">
import type { Assignment } from "~/types";

interface Props {
  open: boolean;
  assignment: Assignment | null;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (
    e: "submit",
    data: {
      title: string;
      description: string;
      max_score: number;
      due_date: string;
      is_required: boolean;
      allow_late_submission: boolean;
    }
  ): void;
}>();

const form = reactive({
  title: "",
  description: "",
  max_score: 100,
  due_date: "",
  is_required: false,
  allow_late_submission: true,
});

const isSubmitting = ref(false);

// Форматирование даты для input datetime-local
const formatDateForInput = (dateString: string | null | undefined): string => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return date.toISOString().slice(0, 16);
};

// Синхронизация формы при открытии
watch(
  () => props.assignment,
  (assignment) => {
    if (assignment) {
      form.title = assignment.title;
      form.description = assignment.description || "";
      form.max_score = assignment.max_score;
      form.due_date = formatDateForInput(assignment.due_date);
      form.is_required = assignment.is_required;
      form.allow_late_submission = assignment.allow_late_submission;
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
      <div class="p-6 max-w-lg">
        <h3 class="text-xl font-semibold text-default mb-6">
          Редактировать задание
        </h3>

        <form class="space-y-4" @submit.prevent="handleSubmit">
          <UFormField label="Название задания" required size="lg">
            <UInput
              v-model="form.title"
              placeholder="Практическое задание #1"
              class="w-full"
              size="lg"
            />
          </UFormField>

          <UFormField label="Описание" size="lg">
            <UTextarea
              v-model="form.description"
              placeholder="О чём это задание"
              :rows="3"
              class="w-full"
              size="lg"
            />
          </UFormField>

          <div class="grid grid-cols-2 gap-4">
            <UFormField label="Макс. балл" required size="lg">
              <UInput
                v-model.number="form.max_score"
                type="number"
                :min="1"
                :max="1000"
                class="w-full"
                size="lg"
              />
            </UFormField>

            <UFormField label="Срок сдачи" size="lg">
              <UInput
                v-model="form.due_date"
                type="datetime-local"
                class="w-full"
                size="lg"
              />
            </UFormField>
          </div>

          <div class="space-y-3 pt-2">
            <UCheckbox
              v-model="form.is_required"
              label="Обязательное задание"
              description="Студент должен сдать для прохождения курса"
            />

            <UCheckbox
              v-model="form.allow_late_submission"
              label="Разрешить сдачу после срока"
              description="Будет отмечено как просроченное"
            />
          </div>

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
