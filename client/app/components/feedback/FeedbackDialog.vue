<script lang="ts" setup>
import { z } from "zod";
import {
  createFeedbackSchema,
  FEEDBACK_TYPE_LABELS,
} from "~/schemas/feedback.schema";
import type { FormSubmitEvent } from "#ui/types";

const model = defineModel<boolean>({ required: true });

const { createFeedback } = useFeedbackService();
const toast = useToast();

const feedbackTypes = Object.entries(FEEDBACK_TYPE_LABELS).map(
  ([value, label]) => ({
    value,
    label,
  })
);

type Schema = z.output<typeof createFeedbackSchema>;

const state = reactive<Schema>({
  feedback_type: "other",
  title: "",
  description: "",
  screenshot: undefined,
});

const isSubmitting = ref(false);
const fileInputRef = ref<HTMLInputElement>();
const selectedFileName = ref<string>("");

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    // Проверяем размер файла (макс 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.add({
        title: "Файл слишком большой",
        description: "Максимальный размер файла — 5 МБ",
        color: "error",
      });
      return;
    }

    // Проверяем тип файла
    if (!file.type.startsWith("image/")) {
      toast.add({
        title: "Неверный тип файла",
        description: "Можно прикреплять только изображения",
        color: "error",
      });
      return;
    }

    state.screenshot = file;
    selectedFileName.value = file.name;
  }
};

const removeFile = () => {
  state.screenshot = undefined;
  selectedFileName.value = "";
  if (fileInputRef.value) {
    fileInputRef.value.value = "";
  }
};

const onSubmit = async (event: FormSubmitEvent<Schema>) => {
  try {
    isSubmitting.value = true;

    await createFeedback(event.data);

    toast.add({
      title: "Спасибо за отзыв!",
      description: "Мы обязательно рассмотрим ваше обращение",
      color: "success",
    });

    // Сброс формы
    state.feedback_type = "other";
    state.title = "";
    state.description = "";
    removeFile();

    model.value = false;
  } catch (error: any) {
    toast.add({
      title: "Ошибка отправки",
      description: error.message || "Не удалось отправить отзыв",
      color: "error",
    });
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <UModal
    v-model:open="model"
    title="Обратная связь"
    description="Расскажите нам о проблеме, предложите улучшение или задайте вопрос"
  >
    <template #body>
      <UForm
        id="feedback-form"
        :schema="createFeedbackSchema"
        :state="state"
        class="flex flex-col gap-4 w-full"
        @submit="onSubmit"
      >
        <!-- Тип обращения -->
        <UFormField
          label="Тип обращения"
          name="feedback_type"
          required
          :ui="{ label: 'text-base font-semibold' }"
        >
          <USelect
            v-model="state.feedback_type"
            :options="feedbackTypes"
            placeholder="Выберите тип"
            size="lg"
            class="w-full"
            :ui="{ base: 'text-base py-2 px-4' }"
          />
        </UFormField>

        <!-- Заголовок -->
        <UFormField
          label="Заголовок"
          name="title"
          required
          :ui="{ label: 'text-base font-semibold' }"
        >
          <UInput
            v-model="state.title"
            placeholder="Краткое описание проблемы"
            size="lg"
            maxlength="200"
            class="w-full"
            :ui="{ base: 'text-base py-2 px-4' }"
          />
        </UFormField>

        <!-- Описание -->
        <UFormField
          label="Описание"
          name="description"
          required
          :ui="{ label: 'text-base font-semibold' }"
        >
          <UTextarea
            v-model="state.description"
            placeholder="Подробно опишите ситуацию..."
            :rows="6"
            size="lg"
            maxlength="2000"
            autoresize
            class="w-full"
            :ui="{ base: 'text-base py-2 px-4' }"
          />
        </UFormField>

        <!-- Прикрепить файл -->
        <UFormField
          label="Прикрепить скриншот"
          name="screenshot"
          hint="PNG, JPG, макс 5 МБ"
          :ui="{ label: 'text-base font-semibold' }"
        >
          <div class="space-y-2">
            <input
              ref="fileInputRef"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleFileChange"
            />

            <UButton
              v-if="!selectedFileName"
              icon="heroicons:photo"
              variant="outline"
              color="neutral"
              block
              size="lg"
              @click="fileInputRef?.click()"
            >
              Выбрать файл
            </UButton>

            <div
              v-else
              class="flex items-center justify-between rounded-lg border border-default-200 bg-default-50 p-3"
            >
              <div class="flex items-center gap-2">
                <UIcon name="heroicons:photo" class="size-5 text-primary-500" />
                <span class="text-sm font-medium">{{ selectedFileName }}</span>
              </div>
              <UButton
                icon="heroicons:x-mark"
                variant="ghost"
                color="neutral"
                size="xs"
                @click="removeFile"
              />
            </div>
          </div>
        </UFormField>
      </UForm>
    </template>

    <template #footer>
      <div class="flex justify-end gap-2 w-full">
        <UButton
          type="button"
          variant="outline"
          color="neutral"
          @click="model = false"
        >
          Отмена
        </UButton>
        <UButton
          type="submit"
          form="feedback-form"
          :loading="isSubmitting"
          :disabled="isSubmitting"
        >
          Отправить
        </UButton>
      </div>
    </template>
  </UModal>
</template>
