<script setup lang="ts">
import type { SubmissionDetail } from "~/types";

const props = defineProps<{
  submission?: SubmissionDetail | null;
  hasSubmission: boolean;
  canEdit: boolean;
  canSubmit: boolean;
}>();

const emit = defineEmits<{
  (e: "submit", payload: { content: string; file: File | null }): void;
}>();

const isEditing = ref(false);
const content = ref(props.submission?.content || "");
const uploadedFile = ref<File | null>(null);
const fileInput = ref<HTMLInputElement>();

// Initialize edit mode for new submissions
watch(
  () => props.hasSubmission,
  (val) => {
    if (!val) isEditing.value = true;
  },
  { immediate: true }
);

const formatDate = (date: string | null | undefined): string => {
  if (!date) return "";
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date));
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const startEditing = () => {
  content.value = props.submission?.content || "";
  isEditing.value = true;
};

const cancelEditing = () => {
  content.value = props.submission?.content || "";
  uploadedFile.value = null;
  isEditing.value = false;
};

const handleFileDrop = (event: DragEvent) => {
  event.preventDefault();
  const files = event.dataTransfer?.files;
  if (files && files.length > 0 && files[0]) {
    uploadedFile.value = files[0];
  }
};

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files.length > 0 && input.files[0]) {
    uploadedFile.value = input.files[0];
  }
};

const removeFile = () => {
  uploadedFile.value = null;
};

const handleSubmit = () => {
  emit("submit", { content: content.value, file: uploadedFile.value });
  uploadedFile.value = null;
  isEditing.value = false;
};

// Expose for parent to reset state after successful submission
defineExpose({
  resetForm: () => {
    uploadedFile.value = null;
    isEditing.value = false;
  },
});
</script>

<template>
  <UCard>
    <template #header>
      <h2 class="text-2xl font-semibold text-default flex items-center gap-2">
        <UIcon name="i-lucide-send" class="size-6 text-primary" />
        {{ hasSubmission ? "Ваш ответ" : "Сдать задание" }}
      </h2>
    </template>

    <div class="flex items-center justify-between">
      <UButton
        v-if="hasSubmission && canEdit && !isEditing"
        color="neutral"
        variant="ghost"
        size="sm"
        icon="i-lucide-pencil"
        @click="startEditing"
      >
        Редактировать
      </UButton>
    </div>

    <div class="px-3">
      <!-- View Mode -->
      <template v-if="hasSubmission && !isEditing">
        <div class="space-y-4">
          <div
            v-if="submission!.content"
            class="prose prose-sm max-w-none text-default"
          >
            {{ submission!.content }}
          </div>

          <div v-if="submission!.files && submission!.files.length > 0">
            <p class="text-sm text-muted mb-2">Прикреплённые файлы:</p>
            <div class="flex flex-wrap gap-2">
              <a
                v-for="file in submission!.files"
                :key="file.id"
                :href="file.file_url"
                target="_blank"
                class="inline-flex items-center gap-2 px-3 py-2 bg-muted/10 rounded-lg text-sm hover:bg-muted/20 transition-colors"
              >
                <UIcon name="i-lucide-file" class="size-4" />
                {{ file.filename }}
              </a>
            </div>
          </div>

          <div class="pt-4 border-t border-default text-sm text-muted">
            <p>
              Отправлено: {{ formatDate(submission!.submitted_at) }}
              <UBadge
                v-if="submission!.is_late"
                color="warning"
                variant="soft"
                size="sm"
                class="ml-2"
              >
                С опозданием
              </UBadge>
            </p>
          </div>
        </div>
      </template>

      <!-- Edit/Create Mode -->
      <template v-else-if="canSubmit || isEditing">
        <form class="space-y-6" @submit.prevent="handleSubmit">
          <div>
            <label class="block text-xl font-medium text-default mb-2">
              Ваш ответ
            </label>
            <UTextarea
              v-model="content"
              placeholder="Напишите ваш ответ здесь..."
              :rows="6"
              size="xl"
              class="w-full"
            />
          </div>

          <div>
            <label class="block text-xl font-medium text-default mb-2">
              Файлы (опционально)
            </label>
            <div
              class="border-2 border-dashed border-default rounded-xl p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
              @dragover.prevent
              @drop="handleFileDrop"
              @click="fileInput?.click()"
            >
              <input
                ref="fileInput"
                type="file"
                size="xl"
                class="hidden"
                @change="handleFileSelect"
              />
              <UIcon
                name="i-lucide-upload-cloud"
                class="size-10 text-muted mx-auto mb-3"
              />
              <p class="text-muted">
                Перетащите файлы сюда или
                <span class="text-primary">выберите</span>
              </p>
              <p class="text-xs text-muted mt-1">PDF, DOC, ZIP до 10MB</p>
            </div>

            <div v-if="uploadedFile" class="mt-4">
              <div
                class="flex items-center gap-3 px-4 py-2 bg-muted/10 rounded-lg"
              >
                <UIcon name="i-lucide-file" class="size-4 text-muted" />
                <span class="flex-1 text-sm truncate">{{
                  uploadedFile.name
                }}</span>
                <span class="text-xs text-muted">{{
                  formatFileSize(uploadedFile.size)
                }}</span>
                <UButton
                  color="error"
                  variant="ghost"
                  size="xs"
                  icon="i-lucide-x"
                  @click="removeFile"
                />
              </div>
            </div>
          </div>

          <div
            class="flex items-center justify-end gap-3 pt-4 border-t border-default"
          >
            <UButton
              v-if="hasSubmission"
              type="button"
              color="neutral"
              variant="ghost"
              @click="cancelEditing"
            >
              Отмена
            </UButton>
            <slot name="submit-button">
              <UButton
                type="submit"
                size="lg"
                color="primary"
                icon="i-lucide-send"
              >
                {{ hasSubmission ? "Обновить ответ" : "Отправить" }}
              </UButton>
            </slot>
          </div>
        </form>
      </template>

      <!-- Cannot Submit -->
      <template v-else>
        <div class="text-center py-8">
          <UIcon
            name="i-lucide-clock"
            class="size-12 text-error mx-auto mb-3"
          />
          <h3 class="text-lg font-semibold text-default mb-2">
            Срок сдачи истёк
          </h3>
          <p class="text-muted">
            К сожалению, вы не можете сдать это задание после срока
          </p>
        </div>
      </template>
    </div>
  </UCard>
</template>
