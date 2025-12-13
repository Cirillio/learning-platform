<script setup lang="ts">
interface Props {
  modelValue: File[];
  accept?: string;
  maxSize?: number; // in MB
  maxFiles?: number;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  accept: "*",
  maxSize: 10,
  maxFiles: 5,
  disabled: false,
});

const emit = defineEmits<{
  "update:modelValue": [files: File[]];
}>();

const toast = useToast();
const fileInput = ref<HTMLInputElement | null>(null);
const isDragging = ref(false);

// Format file size
const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

// Validate file
const validateFile = (file: File): boolean => {
  // Size check
  if (file.size > props.maxSize * 1024 * 1024) {
    toast.add({
      title: "Файл слишком большой",
      description: `Максимальный размер: ${props.maxSize} MB`,
      color: "error",
    });
    return false;
  }

  return true;
};

// Add files
const addFiles = (newFiles: FileList | File[]) => {
  const filesArray = Array.from(newFiles);

  // Max files check
  if (props.modelValue.length + filesArray.length > props.maxFiles) {
    toast.add({
      title: "Слишком много файлов",
      description: `Максимум ${props.maxFiles} файлов`,
      color: "error",
    });
    return;
  }

  const validFiles = filesArray.filter(validateFile);
  if (validFiles.length > 0) {
    emit("update:modelValue", [...props.modelValue, ...validFiles]);
  }
};

// Remove file
const removeFile = (index: number) => {
  const newFiles = [...props.modelValue];
  newFiles.splice(index, 1);
  emit("update:modelValue", newFiles);
};

// Handle file input change
const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    addFiles(input.files);
    input.value = ""; // Reset input
  }
};

// Handle drag events
const handleDragEnter = (e: DragEvent) => {
  e.preventDefault();
  if (!props.disabled) {
    isDragging.value = true;
  }
};

const handleDragLeave = (e: DragEvent) => {
  e.preventDefault();
  isDragging.value = false;
};

const handleDragOver = (e: DragEvent) => {
  e.preventDefault();
};

const handleDrop = (e: DragEvent) => {
  e.preventDefault();
  isDragging.value = false;

  if (props.disabled) return;

  if (e.dataTransfer?.files) {
    addFiles(e.dataTransfer.files);
  }
};

// Click to upload
const openFileDialog = () => {
  if (!props.disabled) {
    fileInput.value?.click();
  }
};

// Get file icon based on type
const getFileIcon = (file: File): string => {
  const type = file.type;
  if (type.startsWith("image/")) return "i-lucide-image";
  if (type.startsWith("video/")) return "i-lucide-video";
  if (type.includes("pdf")) return "i-lucide-file-text";
  if (type.includes("word") || type.includes("document"))
    return "i-lucide-file-text";
  if (type.includes("excel") || type.includes("spreadsheet"))
    return "i-lucide-table";
  if (type.includes("zip") || type.includes("rar") || type.includes("archive"))
    return "i-lucide-archive";
  return "i-lucide-file";
};
</script>

<template>
  <div>
    <!-- Hidden file input -->
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      multiple
      class="hidden"
      @change="handleFileChange"
    />

    <!-- Drop Zone -->
    <div
      class="border-2 border-dashed rounded-xl p-8 text-center transition-all cursor-pointer"
      :class="[
        isDragging
          ? 'border-primary bg-primary/5'
          : 'border-default hover:border-primary/50',
        disabled ? 'opacity-50 cursor-not-allowed' : '',
      ]"
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
      @dragover="handleDragOver"
      @drop="handleDrop"
      @click="openFileDialog"
    >
      <UIcon
        :name="isDragging ? 'i-lucide-download' : 'i-lucide-upload-cloud'"
        class="size-10 mx-auto mb-3"
        :class="isDragging ? 'text-primary' : 'text-muted'"
      />
      <p class="text-muted">
        <span v-if="isDragging" class="text-primary font-medium"
          >Отпустите файлы</span
        >
        <template v-else>
          Перетащите файлы сюда или
          <span class="text-primary font-medium">выберите</span>
        </template>
      </p>
      <p class="text-xs text-muted mt-1">
        До {{ maxFiles }} файлов, максимум {{ maxSize }} MB каждый
      </p>
    </div>

    <!-- Files List -->
    <div v-if="modelValue.length > 0" class="mt-4 space-y-2">
      <div
        v-for="(file, index) in modelValue"
        :key="index"
        class="flex items-center gap-3 px-4 py-3 bg-muted/10 rounded-lg group"
      >
        <UIcon :name="getFileIcon(file)" class="size-5 text-primary shrink-0" />
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-default truncate">
            {{ file.name }}
          </p>
          <p class="text-xs text-muted">
            {{ formatFileSize(file.size) }}
          </p>
        </div>
        <UButton
          icon="i-lucide-x"
          color="error"
          variant="ghost"
          size="xs"
          class="opacity-0 group-hover:opacity-100 transition-opacity"
          @click.stop="removeFile(index)"
        />
      </div>
    </div>
  </div>
</template>
