<script setup lang="ts">
import { z } from "zod";
import type { Assignment, Lesson } from "~/types";

interface Props {
  assignment?: Assignment | null;
  lessons: Lesson[];
  courseSlug: string;
  isSubmitting?: boolean;
}

interface Emits {
  (e: "submit", data: AssignmentFormData): void;
  (e: "cancel"): void;
}

const props = withDefaults(defineProps<Props>(), {
  assignment: null,
  isSubmitting: false,
});

const emit = defineEmits<Emits>();

const isEditMode = computed(() => !!props.assignment);

// Lessons dropdown options
const lessonOptions = computed(() =>
  props.lessons.map((l) => ({
    label: `${l.order}. ${l.title}`,
    value: l.slug,
  }))
);

// Form Schema
const assignmentSchema = z.object({
  lesson: z.string().min(1, "Выберите урок"),
  title: z
    .string()
    .min(3, "Минимум 3 символа")
    .max(200, "Максимум 200 символов"),
  description: z.string().max(1000, "Максимум 1000 символов").optional(),
  instructions: z.string().max(5000, "Максимум 5000 символов").optional(),
  max_score: z.number().min(1, "Минимум 1").max(1000, "Максимум 1000"),
  due_date: z.string().nullable().optional(),
  is_required: z.boolean(),
  allow_late_submission: z.boolean(),
});

type AssignmentFormData = z.infer<typeof assignmentSchema>;

// Form state
const form = reactive<AssignmentFormData>({
  lesson: props.assignment?.lesson || "",
  title: props.assignment?.title || "",
  description: props.assignment?.description || "",
  instructions: props.assignment?.instructions || "",
  max_score: props.assignment?.max_score || 100,
  due_date: props.assignment?.due_date || null,
  is_required: props.assignment?.is_required || false,
  allow_late_submission: props.assignment?.allow_late_submission || false,
});

// Watch for assignment changes (edit mode)
watch(
  () => props.assignment,
  (newAssignment) => {
    if (newAssignment) {
      form.lesson = newAssignment.lesson;
      form.title = newAssignment.title;
      form.description = newAssignment.description || "";
      form.instructions = newAssignment.instructions || "";
      form.max_score = newAssignment.max_score;
      form.due_date = newAssignment.due_date || null;
      form.is_required = newAssignment.is_required;
      form.allow_late_submission = newAssignment.allow_late_submission;
    }
  },
  { immediate: true }
);

// Computed
const descriptionLength = computed(() => form.description?.length || 0);
const instructionsLength = computed(() => form.instructions?.length || 0);

// Date picker
const formatDateForInput = (date: Date) => {
  return date.toISOString().split("T")[0];
};

const dueDateInputValue = computed({
  get: () => (form.due_date ? form.due_date.split("T")[0] : ""),
  set: (val: string) => {
    form.due_date = val ? new Date(val).toISOString() : null;
  },
});

// Submit handler
const onSubmit = () => {
  emit("submit", { ...form });
};

const onCancel = () => {
  emit("cancel");
};
</script>

<template>
  <UForm
    :schema="assignmentSchema"
    :state="form"
    @submit="onSubmit"
    class="space-y-6"
  >
    <!-- Lesson -->
    <UFormField label="Урок" name="lesson" required>
      <USelect
        v-model="form.lesson"
        :items="lessonOptions"
        placeholder="Выберите урок"
        class="w-full"
        :disabled="isEditMode"
      />
      <template v-if="isEditMode" #hint>
        <span class="text-muted text-xs">
          Нельзя изменить урок после создания
        </span>
      </template>
    </UFormField>

    <!-- Title -->
    <UFormField label="Название задания" name="title" required>
      <UInput
        v-model="form.title"
        placeholder="Введите название задания"
        size="lg"
        class="w-full"
      />
    </UFormField>

    <!-- Description -->
    <UFormField label="Описание" name="description">
      <UTextarea
        v-model="form.description"
        placeholder="Краткое описание задания"
        :rows="3"
        :maxlength="1000"
        class="w-full"
      />
      <template #hint>
        <span :class="descriptionLength > 900 ? 'text-warning' : 'text-muted'">
          {{ descriptionLength }}/1000
        </span>
      </template>
    </UFormField>

    <!-- Instructions -->
    <UFormField label="Инструкции" name="instructions">
      <UTextarea
        v-model="form.instructions"
        placeholder="Подробные инструкции по выполнению задания..."
        :rows="8"
        :maxlength="5000"
        class="w-full"
      />
      <template #hint>
        <span
          :class="instructionsLength > 4500 ? 'text-warning' : 'text-muted'"
        >
          {{ instructionsLength }}/5000
        </span>
      </template>
    </UFormField>

    <!-- Score and Due Date -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Max Score -->
      <UFormField label="Максимальный балл" name="max_score" required>
        <UInput
          v-model.number="form.max_score"
          type="number"
          :min="1"
          :max="1000"
          placeholder="100"
          class="w-full"
        >
          <template #trailing>
            <span class="text-muted text-sm">баллов</span>
          </template>
        </UInput>
      </UFormField>

      <!-- Due Date -->
      <UFormField label="Срок сдачи" name="due_date">
        <UInput v-model="dueDateInputValue" type="date" class="w-full">
          <template #leading>
            <UIcon name="i-heroicons-calendar" class="w-4 h-4" />
          </template>
        </UInput>
        <template #hint>
          <button
            v-if="form.due_date"
            type="button"
            class="text-xs text-primary hover:underline"
            @click="form.due_date = null"
          >
            Очистить дату
          </button>
        </template>
      </UFormField>
    </div>

    <!-- Checkboxes -->
    <div class="space-y-4">
      <UFormField name="is_required">
        <UCheckbox v-model="form.is_required" label="Обязательное задание">
          <template #description>
            <span class="text-muted text-sm">
              Студент должен выполнить это задание для завершения курса
            </span>
          </template>
        </UCheckbox>
      </UFormField>

      <UFormField name="allow_late_submission">
        <UCheckbox
          v-model="form.allow_late_submission"
          label="Разрешить поздн сдачу"
        >
          <template #description>
            <span class="text-muted text-sm">
              Студенты смогут сдавать задание после истечения срока
            </span>
          </template>
        </UCheckbox>
      </UFormField>
    </div>

    <!-- Actions -->
    <div
      class="flex items-center justify-end gap-3 pt-4 border-t border-default"
    >
      <UButton
        type="button"
        variant="ghost"
        color="neutral"
        @click="onCancel"
        :disabled="isSubmitting"
      >
        Отмена
      </UButton>
      <UButton
        type="submit"
        color="primary"
        :loading="isSubmitting"
        :disabled="isSubmitting"
      >
        {{ isEditMode ? "Сохранить изменения" : "Создать задание" }}
      </UButton>
    </div>
  </UForm>
</template>
