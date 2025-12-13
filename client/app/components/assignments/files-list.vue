<script setup lang="ts">
import type { AssignmentFile } from "~/types";

defineProps<{
  files: AssignmentFile[];
}>();

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};
</script>

<template>
  <div class="bg-elevated rounded-xl border border-default overflow-hidden">
    <div class="px-6 py-4 border-b border-default">
      <h2 class="text-lg font-semibold text-default flex items-center gap-2">
        <UIcon name="i-lucide-paperclip" class="size-5 text-primary" />
        Прикреплённые файлы
      </h2>
    </div>
    <div class="divide-y divide-default">
      <a
        v-for="file in files"
        :key="file.id"
        :href="file.file_url"
        target="_blank"
        class="flex items-center gap-4 px-6 py-4 hover:bg-muted/5 transition-colors"
      >
        <UIcon name="i-lucide-file" class="size-5 text-muted" />
        <div class="flex-1 min-w-0">
          <p class="font-medium text-default truncate">{{ file.filename }}</p>
          <p class="text-sm text-muted">{{ formatFileSize(file.file_size) }}</p>
        </div>
        <UIcon name="i-lucide-download" class="size-5 text-primary" />
      </a>
    </div>
  </div>
</template>
