<script setup lang="ts">
import type { Assignment } from "~/types";
import { formatFileSize } from "~/utils/formatters.util";

defineProps<{
  files: Assignment["files"];
}>();
</script>

<template>
  <UCard v-if="files && files.length > 0">
    <template #header>
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-paperclip" class="size-5 text-primary" />
        <h3 class="font-semibold">
          Файлы задания ({{ files.length }})
        </h3>
      </div>
    </template>
    <div class="space-y-2">
      <div
        v-for="file in files"
        :key="file.id"
        class="flex items-center justify-between p-3 bg-elevated rounded-lg hover:bg-muted/50 transition-colors"
      >
        <div class="flex items-center gap-3">
          <div class="p-2 bg-primary/10 rounded-lg">
            <UIcon name="i-lucide-file" class="size-5 text-primary" />
          </div>
          <div>
            <div class="font-medium">{{ file.filename }}</div>
            <div class="text-xs text-muted">
              {{ formatFileSize(file.file_size) }}
            </div>
          </div>
        </div>
        <UButton
          :to="file.file_url"
          target="_blank"
          color="neutral"
          variant="ghost"
          icon="i-lucide-download"
          size="sm"
        >
          Скачать
        </UButton>
      </div>
    </div>
  </UCard>
</template>
