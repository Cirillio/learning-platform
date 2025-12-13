<script setup lang="ts">
import type { SubmissionDetail } from "~/types";

interface Props {
  submission: SubmissionDetail;
}

defineProps<Props>();

// Format helpers
const formatDate = (date: string) => {
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

// Get file icon
const getFileIcon = (filename: string): string => {
  const ext = filename.split(".").pop()?.toLowerCase();
  if (["jpg", "jpeg", "png", "gif", "webp"].includes(ext || ""))
    return "i-lucide-image";
  if (["mp4", "webm", "avi", "mov"].includes(ext || ""))
    return "i-lucide-video";
  if (ext === "pdf") return "i-lucide-file-text";
  if (["doc", "docx"].includes(ext || "")) return "i-lucide-file-text";
  if (["xls", "xlsx"].includes(ext || "")) return "i-lucide-table";
  if (["zip", "rar", "7z"].includes(ext || "")) return "i-lucide-archive";
  return "i-lucide-file";
};
</script>

<template>
  <div class="space-y-6">
    <!-- Student Info -->
    <div class="flex items-center gap-4 pb-4 border-b border-default">
      <UAvatar :alt="submission.student_name" size="lg" />
      <div>
        <h3 class="font-semibold text-default text-lg">
          {{ submission.student_name }}
        </h3>
        <p class="text-sm text-muted">
          Отправлено: {{ formatDate(submission.submitted_at) }}
        </p>
      </div>
      <div class="ml-auto flex items-center gap-2">
        <UBadge
          :color="
            submission.status === 'graded'
              ? 'success'
              : submission.status === 'pending'
              ? 'warning'
              : 'info'
          "
          variant="soft"
        >
          {{
            submission.status === "graded"
              ? "Оценено"
              : submission.status === "pending"
              ? "На проверке"
              : "Возвращено"
          }}
        </UBadge>
        <UBadge v-if="submission.is_late" color="error" variant="soft">
          С опозданием
        </UBadge>
      </div>
    </div>

    <!-- Content -->
    <div>
      <h4 class="text-sm font-medium text-muted mb-3 flex items-center gap-2">
        <UIcon name="i-lucide-file-text" class="size-4" />
        Текстовый ответ
      </h4>
      <div
        v-if="submission.content"
        class="bg-muted/5 rounded-xl p-6 prose prose-sm max-w-none text-default whitespace-pre-wrap"
      >
        {{ submission.content }}
      </div>
      <div
        v-else
        class="bg-muted/5 rounded-xl p-6 text-center text-muted italic"
      >
        Текстовый ответ не предоставлен
      </div>
    </div>

    <!-- Files -->
    <div v-if="submission.files && submission.files.length > 0">
      <h4 class="text-sm font-medium text-muted mb-3 flex items-center gap-2">
        <UIcon name="i-lucide-paperclip" class="size-4" />
        Прикреплённые файлы ({{ submission.files.length }})
      </h4>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <a
          v-for="file in submission.files"
          :key="file.id"
          :href="file.file_url"
          target="_blank"
          class="flex items-center gap-3 p-4 bg-muted/5 rounded-xl hover:bg-muted/10 transition-colors group"
        >
          <div
            class="size-10 rounded-lg bg-primary/10 flex items-center justify-center shrink-0"
          >
            <UIcon
              :name="getFileIcon(file.filename)"
              class="size-5 text-primary"
            />
          </div>
          <div class="flex-1 min-w-0">
            <p
              class="font-medium text-default truncate group-hover:text-primary transition-colors"
            >
              {{ file.filename }}
            </p>
            <p class="text-xs text-muted">
              {{ formatFileSize(file.file_size) }}
            </p>
          </div>
          <UIcon
            name="i-lucide-external-link"
            class="size-4 text-muted group-hover:text-primary transition-colors shrink-0"
          />
        </a>
      </div>
    </div>

    <!-- Meta Info -->
    <div
      class="flex items-center gap-6 text-sm text-muted pt-4 border-t border-default"
    >
      <span class="flex items-center gap-2">
        <UIcon name="i-lucide-clock" class="size-4" />
        Обновлено: {{ formatDate(submission.updated_at) }}
      </span>
      <span class="flex items-center gap-2">
        <UIcon name="i-lucide-paperclip" class="size-4" />
        {{ submission.files_count || submission.files?.length || 0 }} файлов
      </span>
    </div>
  </div>
</template>
