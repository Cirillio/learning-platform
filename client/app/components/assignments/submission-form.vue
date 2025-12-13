<script setup lang="ts">
import type { SubmissionDetail } from "~/types";

const props = defineProps<{
  submission?: SubmissionDetail | null;
  hasSubmission: boolean;
  canEdit: boolean;
  canSubmit: boolean;
}>();

const emit = defineEmits<{
  (e: "submit", payload: { content: string; files: File[] }): void;
}>();

const isEditing = ref(false);
const content = ref(props.submission?.content || "");
const uploadedFiles = ref<File[]>([]);
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
  uploadedFiles.value = [];
  isEditing.value = false;
};

const handleFileDrop = (event: DragEvent) => {
  event.preventDefault();
  const files = event.dataTransfer?.files;
  if (files) {
    uploadedFiles.value = [...uploadedFiles.value, ...Array.from(files)];
  }
};

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    uploadedFiles.value = [...uploadedFiles.value, ...Array.from(input.files)];
  }
};

const removeFile = (index: number) => {
  uploadedFiles.value.splice(index, 1);
};

const handleSubmit = () => {
  emit("submit", { content: content.value, files: uploadedFiles.value });
  uploadedFiles.value = [];
  isEditing.value = false;
};

// Expose for parent to reset state after successful submission
defineExpose({
  resetForm: () => {
    uploadedFiles.value = [];
    isEditing.value = false;
  },
});
</script>

<template>
  <div class="bg-elevated rounded-xl border border-default overflow-hidden">
    <div
      class="px-6 py-4 border-b border-default flex items-center justify-between"
    >
      <h2 class="text-lg font-semibold text-default flex items-center gap-2">
        <UIcon name="i-lucide-send" class="size-5 text-primary" />
        {{ hasSubmission ? "Ваш ответ" : "Сдать задание" }}
      </h2>

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

    <div class="p-6 lg:p-8">
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
            <label class="block text-sm font-medium text-default mb-2">
              Ваш ответ
            </label>
            <UTextarea
              v-model="content"
              placeholder="Напишите ваш ответ здесь..."
              :rows="6"
              class="w-full"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-default mb-2">
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
                multiple
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

            <div v-if="uploadedFiles.length > 0" class="mt-4 space-y-2">
              <div
                v-for="(file, index) in uploadedFiles"
                :key="index"
                class="flex items-center gap-3 px-4 py-2 bg-muted/10 rounded-lg"
              >
                <UIcon name="i-lucide-file" class="size-4 text-muted" />
                <span class="flex-1 text-sm truncate">{{ file.name }}</span>
                <span class="text-xs text-muted">{{
                  formatFileSize(file.size)
                }}</span>
                <UButton
                  color="error"
                  variant="ghost"
                  size="xs"
                  icon="i-lucide-x"
                  @click="removeFile(index)"
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
              <UButton type="submit" color="primary" icon="i-lucide-send">
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
  </div>
</template>
