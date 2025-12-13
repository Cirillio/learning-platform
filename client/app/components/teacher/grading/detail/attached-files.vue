<script setup lang="ts">
import type { SubmissionFile } from "~/types";

defineProps<{
  files: SubmissionFile[];
}>();

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};
</script>

<template>
  <UCard v-if="files && files.length > 0">
    <template #header>
      <h2 class="text-lg font-semibold text-default">
        Прикреплённые файлы ({{ files.length }})
      </h2>
    </template>
    <div class="divide-y divide-default">
      <a
        v-for="file in files"
        :key="file.id"
        :href="file.file_url"
        target="_blank"
        class="flex items-center gap-4 px-6 py-4 hover:bg-muted/5 transition-colors"
      >
        <div
          class="size-10 rounded-lg bg-primary/10 flex items-center justify-center"
        >
          <UIcon name="i-lucide-file" class="size-5 text-primary" />
        </div>
        <div class="flex-1 min-w-0">
          <p class="font-medium text-default truncate">
            {{ file.filename }}
          </p>
          <p class="text-sm text-muted">
            {{ formatFileSize(file.file_size) }}
          </p>
        </div>
        <UIcon name="i-lucide-download" class="size-5 text-primary" />
      </a>
    </div>
  </UCard>
</template>
