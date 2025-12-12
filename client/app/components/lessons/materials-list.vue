<script setup lang="ts">
import type { LessonMaterial } from "~/types";

interface Props {
  materials: LessonMaterial[];
}

defineProps<Props>();

// Иконки по типу файла
const getFileIcon = (fileType: string): string => {
  const icons: Record<string, string> = {
    pdf: "i-lucide-file-text",
    doc: "i-lucide-file-text",
    docx: "i-lucide-file-text",
    xls: "i-lucide-sheet",
    xlsx: "i-lucide-sheet",
    ppt: "i-lucide-presentation",
    pptx: "i-lucide-presentation",
    zip: "i-lucide-archive",
    rar: "i-lucide-archive",
    mp4: "i-lucide-video",
    webm: "i-lucide-video",
    mp3: "i-lucide-music",
    wav: "i-lucide-music",
    png: "i-lucide-image",
    jpg: "i-lucide-image",
    jpeg: "i-lucide-image",
    gif: "i-lucide-image",
    svg: "i-lucide-image",
  };

  return icons[fileType.toLowerCase()] || "i-lucide-file";
};

// Форматирование размера файла
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
};

// Скачивание файла
const downloadMaterial = (material: LessonMaterial) => {
  const link = document.createElement("a");
  link.href = material.file_url;
  link.download = material.title;
  link.target = "_blank";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<template>
  <section>
    <UCard class="dark:bg-muted/25 bg-muted/75">
      <!-- Section Header -->
      <div class="p-6 border-b border-default">
        <div class="flex items-center gap-3">
          <div
            class="size-10 rounded-lg bg-info/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-paperclip" class="size-5 text-info" />
          </div>
          <div>
            <h3 class="font-semibold text-default">Материалы урока</h3>
            <p class="text-sm text-muted">{{ materials.length }} файлов</p>
          </div>
        </div>
      </div>

      <!-- Materials List -->
      <div class="divide-y divide-default">
        <div
          v-for="material in materials"
          :key="material.id"
          class="p-4 flex items-center gap-4 hover:bg-muted/50 transition-colors group"
        >
          <!-- File Icon -->
          <div
            class="size-12 rounded-lg bg-muted flex items-center justify-center group-hover:bg-primary/10 transition-colors"
          >
            <UIcon
              :name="getFileIcon(material.file_type)"
              class="size-6 text-muted group-hover:text-primary transition-colors"
            />
          </div>

          <!-- File Info -->
          <div class="flex-1 min-w-0">
            <h4 class="font-medium text-default truncate">
              {{ material.title }}
            </h4>
            <p class="text-sm text-muted">
              {{ material.file_type.toUpperCase() }} •
              {{ formatFileSize(material.file_size) }}
            </p>
            <p
              v-if="material.description"
              class="text-sm text-dimmed mt-1 line-clamp-1"
            >
              {{ material.description }}
            </p>
          </div>

          <!-- Download Button -->
          <UButton
            variant="soft"
            color="primary"
            icon="i-lucide-download"
            size="sm"
            @click="downloadMaterial(material)"
          >
            <span class="hidden sm:inline">Скачать</span>
          </UButton>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="materials.length === 0" class="p-8 text-center">
        <UIcon
          name="i-lucide-folder-open"
          class="size-12 text-muted mx-auto mb-2"
        />
        <p class="text-muted">Материалы не добавлены</p>
      </div>
    </UCard>
  </section>
</template>
