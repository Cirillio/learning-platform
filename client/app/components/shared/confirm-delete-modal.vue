<script setup lang="ts">
interface Props {
  open: boolean;
  title?: string;
  description?: string;
  itemName?: string;
  loading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  title: "Подтверждение удаления",
  description: "Это действие нельзя отменить.",
  itemName: "",
  loading: false,
});

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (e: "confirm"): void;
}>();

const closeModal = () => emit("update:open", false);
const handleConfirm = () => emit("confirm");
</script>

<template>
  <UModal :open="open" @update:open="emit('update:open', $event)">
    <template #content>
      <div class="p-6">
        <div class="flex items-start gap-4">
          <div
            class="size-12 rounded-full bg-error/10 flex items-center justify-center shrink-0"
          >
            <UIcon name="i-lucide-trash-2" class="size-6 text-error" />
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-xl font-semibold text-default mb-2">
              {{ title }}
            </h3>
            <p class="text-base text-muted">
              {{ description }}
            </p>
            <p v-if="itemName" class="text-base text-default font-medium mt-2">
              «{{ itemName }}»
            </p>
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <UButton
            type="button"
            color="neutral"
            variant="ghost"
            size="lg"
            :disabled="loading"
            @click="closeModal"
          >
            Отмена
          </UButton>
          <UButton
            type="button"
            color="error"
            size="lg"
            :loading="loading"
            icon="i-lucide-trash-2"
            @click="handleConfirm"
          >
            Удалить
          </UButton>
        </div>
      </div>
    </template>
  </UModal>
</template>
