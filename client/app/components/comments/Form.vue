<script setup lang="ts">
import type { Comment } from "~/types";
import { commentFormSchema } from "~/schemas/comment.schema";
import type { FormSubmitEvent } from "#ui/types";
import type { z } from "zod";

type FormData = z.infer<typeof commentFormSchema>;

const props = defineProps<{
  /** Режим редактирования (передаем комментарий) */
  editComment?: Comment | null;
  /** ID родительского комментария (для ответа) */
  parentId?: number | null;
  /** Placeholder текста */
  placeholder?: string;
  /** Показывать ли кнопку отмены */
  showCancel?: boolean;
  /** Состояние загрузки */
  loading?: boolean;
}>();

const emit = defineEmits<{
  (e: "submit", text: string, parentId?: number | null): void;
  (e: "cancel"): void;
}>();

// Form state
const state = reactive<FormData>({
  text: props.editComment?.text || "",
});

// Watch для обновления при изменении editComment
watch(
  () => props.editComment,
  (newComment) => {
    state.text = newComment?.text || "";
  }
);

// Computed
const isEditing = computed(() => !!props.editComment);
const charCount = computed(() => state.text.length);
const maxChars = 1000;
const isOverLimit = computed(() => charCount.value > maxChars);

const buttonLabel = computed(() => {
  if (isEditing.value) return "Сохранить";
  if (props.parentId) return "Ответить";
  return "Отправить";
});

const placeholderText = computed(() => {
  if (props.placeholder) return props.placeholder;
  if (isEditing.value) return "Редактирование комментария...";
  if (props.parentId) return "Напишите ответ...";
  return "Напишите комментарий...";
});

// Submit handler
const onSubmit = (event: FormSubmitEvent<FormData>) => {
  if (isOverLimit.value) return;
  emit("submit", event.data.text.trim(), props.parentId);
  
  // Очищаем форму если не редактирование
  if (!isEditing.value) {
    state.text = "";
  }
};

// Cancel handler
const onCancel = () => {
  state.text = props.editComment?.text || "";
  emit("cancel");
};

// Focus на textarea при монтировании (если это ответ или редактирование)
const textareaRef = ref<HTMLTextAreaElement | null>(null);

onMounted(() => {
  if (props.parentId || props.editComment) {
    nextTick(() => {
      textareaRef.value?.focus();
    });
  }
});
</script>

<template>
  <UForm
    :schema="commentFormSchema"
    :state="state"
    class="space-y-3"
    @submit="onSubmit"
  >
    <UFormField name="text">
      <UTextarea
        ref="textareaRef"
        v-model="state.text"
        :placeholder="placeholderText"
        :rows="parentId || editComment ? 2 : 3"
        :maxlength="maxChars + 100"
        autoresize
        class="w-full"
      />
    </UFormField>

    <!-- Footer: счетчик символов + кнопки -->
    <div class="flex items-center justify-between gap-3">
      <!-- Счетчик символов -->
      <span
        class="text-xs"
        :class="isOverLimit ? 'text-error' : 'text-muted'"
      >
        {{ charCount }} / {{ maxChars }}
      </span>

      <!-- Кнопки -->
      <div class="flex items-center gap-2">
        <UButton
          v-if="showCancel || parentId || editComment"
          type="button"
          color="neutral"
          variant="ghost"
          size="sm"
          @click="onCancel"
        >
          Отмена
        </UButton>

        <UButton
          type="submit"
          color="primary"
          size="sm"
          :loading="loading"
          :disabled="!state.text.trim() || isOverLimit || loading"
          icon="i-lucide-send"
        >
          {{ buttonLabel }}
        </UButton>
      </div>
    </div>
  </UForm>
</template>
