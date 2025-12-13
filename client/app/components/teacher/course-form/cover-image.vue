<script setup lang="ts">
defineProps<{
  preview: string | null;
}>();

const emit = defineEmits<{
  (e: "change", file: File): void;
  (e: "remove"): void;
}>();

const fileInput = ref<HTMLInputElement | null>(null);

const handleChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    emit("change", input.files[0]);
  }
};
</script>

<template>
  <UCard>
    <template #header>
      <h2 class="text-lg font-semibold text-default">Обложка курса</h2>
    </template>

    <div
      v-if="!preview"
      class="border-2 border-dashed border-default rounded-xl p-12 text-center hover:border-primary/50 transition-colors cursor-pointer"
      @click="fileInput?.click()"
    >
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleChange"
      />
      <UIcon
        name="i-lucide-image-plus"
        class="size-12 text-muted mx-auto mb-4"
      />
      <p class="text-muted">Нажмите для загрузки или перетащите изображение</p>
      <p class="text-xs text-muted mt-1">
        PNG, JPG до 5MB. Рекомендуемый размер: 1280x720
      </p>
    </div>

    <div v-else class="relative">
      <img
        :src="preview"
        alt="Cover preview"
        class="w-full aspect-video object-cover rounded-xl"
      />
      <UButton
        icon="i-lucide-x"
        color="error"
        variant="solid"
        size="sm"
        class="absolute top-3 right-3"
        @click="emit('remove')"
      />
    </div>
  </UCard>
</template>
