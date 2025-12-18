<script setup lang="ts">
import { z } from "zod";
import type { LessonDetail } from "~/types";

interface Props {
  lesson?: LessonDetail | null;
  courseSlug: string;
  isSubmitting?: boolean;
}

interface Emits {
  (e: "submit", data: LessonFormData): void;
  (e: "cancel"): void;
}

const props = withDefaults(defineProps<Props>(), {
  lesson: null,
  isSubmitting: false,
});

const emit = defineEmits<Emits>();

const isEditMode = computed(() => !!props.lesson);

// Form Schema
const lessonSchema = z.object({
  title: z
    .string()
    .min(3, "Минимум 3 символа")
    .max(200, "Максимум 200 символов"),
  description: z.string().max(500, "Максимум 500 символов").optional(),
  content: z.string().optional(),
  video_url: z
    .string()
    .url("Введите корректный URL")
    .optional()
    .or(z.literal("")),
  duration_minutes: z.number().min(0, "Минимум 0").max(600, "Максимум 600"),
  is_published: z.boolean(),
});

type LessonFormData = z.infer<typeof lessonSchema>;

// Form state
const form = reactive<LessonFormData>({
  title: props.lesson?.title || "",
  description: props.lesson?.description || "",
  content: props.lesson?.content || "",
  video_url: props.lesson?.video_url || "",
  duration_minutes: props.lesson?.duration_minutes || 0,
  is_published: props.lesson?.is_published || false,
});

// Watch for lesson changes (edit mode)
watch(
  () => props.lesson,
  (newLesson) => {
    if (newLesson) {
      form.title = newLesson.title;
      form.description = newLesson.description;
      form.content = newLesson.content || "";
      form.video_url = newLesson.video_url || "";
      form.duration_minutes = newLesson.duration_minutes;
      form.is_published = newLesson.is_published;
    }
  },
  { immediate: true }
);

// Computed
const descriptionLength = computed(() => form.description?.length || 0);
const contentLength = computed(() => form.content?.length || 0);

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
    :schema="lessonSchema"
    :state="form"
    @submit="onSubmit"
    class="space-y-6"
  >
    <!-- Title -->
    <UFormField label="Название урока" name="title" required>
      <UInput
        v-model="form.title"
        placeholder="Введите название урока"
        size="lg"
        class="w-full"
      />
    </UFormField>

    <!-- Description -->
    <UFormField label="Краткое описание" name="description">
      <UTextarea
        v-model="form.description"
        placeholder="Краткое описание урока (отображается в списке)"
        :rows="3"
        :maxlength="500"
        class="w-full"
      />
      <template #hint>
        <span :class="descriptionLength > 450 ? 'text-warning' : 'text-muted'">
          {{ descriptionLength }}/500
        </span>
      </template>
    </UFormField>

    <!-- Content (Markdown) -->
    <UFormField label="Содержание урока" name="content">
      <UTextarea
        v-model="form.content"
        placeholder="Содержание урока в формате Markdown..."
        :rows="12"
        class="w-full font-mono text-sm"
      />
      <template #hint>
        <span class="text-muted">
          Поддерживается Markdown. {{ contentLength }} символов
        </span>
      </template>
    </UFormField>

    <!-- Video URL -->
    <UFormField label="Ссылка на видео" name="video_url">
      <UInput
        v-model="form.video_url"
        placeholder="https://youtube.com/watch?v=..."
        type="url"
        class="w-full"
      >
        <template #leading>
          <UIcon name="i-heroicons-video-camera" class="text-muted" />
        </template>
      </UInput>
      <template #hint>
        <span class="text-muted"
          >YouTube, Vimeo или другие видео-платформы</span
        >
      </template>
    </UFormField>

    <!-- Duration -->
    <UFormField label="Продолжительность (минуты)" name="duration_minutes">
      <UInput
        v-model.number="form.duration_minutes"
        type="number"
        :min="0"
        :max="600"
        placeholder="45"
        class="w-48"
      >
        <template #trailing>
          <span class="text-muted text-sm">мин</span>
        </template>
      </UInput>
    </UFormField>

    <!-- Is Published -->
    <UFormField name="is_published">
      <UCheckbox v-model="form.is_published" label="Опубликовать урок">
        <template #description>
          <span class="text-muted text-sm">
            Опубликованные уроки видны студентам курса
          </span>
        </template>
      </UCheckbox>
    </UFormField>

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
        {{ isEditMode ? "Сохранить изменения" : "Создать урок" }}
      </UButton>
    </div>
  </UForm>
</template>
