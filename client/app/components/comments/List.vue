<script setup lang="ts">
import type { Comment } from "~/types";

const props = defineProps<{
  /** ID урока для загрузки комментариев */
  lessonId: number;
  /** ContentType ID (опционально, будет получен автоматически) */
  contentTypeId?: number;
}>();

const { user, isAuthenticated } = useAuth();

// Composable для работы с комментариями
const {
  comments,
  totalCount,
  isLoading,
  isLoadingMore,
  isSubmitting,
  isEmpty,
  canLoadMore,
  error,
  fetchComments,
  loadMore,
  addComment,
  updateComment,
  deleteComment,
  loadReplies,
} = useComments({
  lessonId: props.lessonId,
  contentTypeId: props.contentTypeId,
});

// UI state
const replyingTo = ref<number | null>(null);
const editingComment = ref<Comment | null>(null);
const deleteConfirmId = ref<number | null>(null);
const showDeleteModal = computed({
  get: () => deleteConfirmId.value !== null,
  set: (val: boolean) => {
    if (!val) deleteConfirmId.value = null;
  },
});

// Загружаем комментарии при монтировании
onMounted(() => {
  if (props.lessonId > 0) {
    fetchComments();
  }
});

// Watch для перезагрузки при смене урока
watch(
  () => props.lessonId,
  (newId) => {
    if (newId > 0) {
      replyingTo.value = null;
      editingComment.value = null;
      fetchComments();
    }
  }
);

// Handlers
const handleSubmitComment = async (text: string, parentId?: number | null) => {
  if (editingComment.value) {
    // Режим редактирования
    await updateComment(editingComment.value.id, text);
    editingComment.value = null;
  } else {
    // Создание нового комментария
    await addComment(text, parentId);
    replyingTo.value = null;
  }
};

const handleReply = (commentId: number) => {
  replyingTo.value = replyingTo.value === commentId ? null : commentId;
  editingComment.value = null;
};

const handleEdit = (comment: Comment) => {
  editingComment.value = comment;
  replyingTo.value = null;
};

const handleCancelEdit = () => {
  editingComment.value = null;
};

const handleDelete = (commentId: number) => {
  deleteConfirmId.value = commentId;
};

const confirmDelete = async () => {
  if (deleteConfirmId.value) {
    await deleteComment(deleteConfirmId.value);
    deleteConfirmId.value = null;
  }
};

const cancelDelete = () => {
  deleteConfirmId.value = null;
};

const handleLoadReplies = async (commentId: number) => {
  await loadReplies(commentId);
};

// Плюрализация для счетчика
const pluralizeComments = (n: number): string => {
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return "комментарий";
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return "комментария";
  return "комментариев";
};
</script>

<template>
  <div class="comments-section space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-semibold text-default flex items-center gap-2">
        <UIcon name="i-lucide-message-square" class="size-5" />
        Комментарии
        <UBadge v-if="totalCount > 0" color="neutral" variant="soft" size="sm">
          {{ totalCount }} {{ pluralizeComments(totalCount) }}
        </UBadge>
      </h3>
    </div>

    <!-- Форма добавления комментария (только для авторизованных) -->
    <div v-if="isAuthenticated" class="mb-6">
      <!-- Режим редактирования -->
      <template v-if="editingComment">
        <div class="flex items-center gap-2 mb-2">
          <UIcon name="i-lucide-pencil" class="size-4 text-muted" />
          <span class="text-sm text-muted">Редактирование комментария</span>
        </div>
        <CommentsForm
          :edit-comment="editingComment"
          :loading="isSubmitting"
          show-cancel
          @submit="handleSubmitComment"
          @cancel="handleCancelEdit"
        />
      </template>

      <!-- Обычная форма -->
      <template v-else>
        <CommentsForm
          :loading="isSubmitting"
          placeholder="Оставьте комментарий к уроку..."
          @submit="handleSubmitComment"
        />
      </template>
    </div>

    <!-- Сообщение для неавторизованных -->
    <UAlert
      v-else
      color="info"
      variant="soft"
      title="Войдите, чтобы оставить комментарий"
      icon="i-lucide-log-in"
    >
      <template #actions>
        <UButton
          to="/auth/login"
          color="primary"
          size="sm"
        >
          Войти
        </UButton>
      </template>
    </UAlert>

    <!-- Loading state -->
    <div v-if="isLoading" class="space-y-4">
      <USkeleton class="h-24 w-full rounded-lg" />
      <USkeleton class="h-24 w-full rounded-lg" />
      <USkeleton class="h-24 w-full rounded-lg" />
    </div>

    <!-- Error state -->
    <UAlert
      v-else-if="error"
      color="error"
      variant="outline"
      title="Ошибка загрузки комментариев"
      :description="error.message"
      icon="i-lucide-alert-circle"
    >
      <template #actions>
        <UButton
          color="error"
          variant="soft"
          size="sm"
          icon="i-lucide-refresh-cw"
          @click="fetchComments()"
        >
          Повторить
        </UButton>
      </template>
    </UAlert>

    <!-- Empty state -->
    <div
      v-else-if="isEmpty"
      class="text-center py-12"
    >
      <UIcon name="i-lucide-message-square-dashed" class="size-12 text-muted mx-auto mb-4" />
      <p class="text-muted">Пока нет комментариев</p>
      <p class="text-sm text-muted mt-1">Будьте первым, кто оставит комментарий!</p>
    </div>

    <!-- Comments list -->
    <div v-else class="space-y-4">
      <TransitionGroup name="list">
        <div v-for="comment in comments" :key="comment.id">
          <CommentsItem
            :comment="comment"
            @reply="handleReply"
            @edit="handleEdit"
            @delete="handleDelete"
            @load-replies="handleLoadReplies"
          />

          <!-- Reply form (встроенная под комментарием) -->
          <Transition name="slide-fade">
            <div
              v-if="replyingTo === comment.id && isAuthenticated"
              class="ml-6 mt-3 pl-4 border-l-2 border-primary/30"
            >
              <div class="flex items-center gap-2 mb-2">
                <UIcon name="i-lucide-corner-down-right" class="size-4 text-muted" />
                <span class="text-sm text-muted">
                  Ответ на комментарий
                  <span class="font-medium text-default">
                    {{ comment.author_name || comment.author.username }}
                  </span>
                </span>
              </div>
              <CommentsForm
                :parent-id="comment.id"
                :loading="isSubmitting"
                show-cancel
                @submit="handleSubmitComment"
                @cancel="replyingTo = null"
              />
            </div>
          </Transition>
        </div>
      </TransitionGroup>

      <!-- Load more button -->
      <div v-if="canLoadMore" class="text-center pt-4">
        <UButton
          color="neutral"
          variant="soft"
          :loading="isLoadingMore"
          icon="i-lucide-chevron-down"
          @click="loadMore"
        >
          Загрузить ещё
        </UButton>
      </div>
    </div>

    <!-- Delete confirmation modal -->
    <UModal v-model:open="showDeleteModal">
      <template #content>
        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-trash-2" class="size-5 text-error" />
              <span class="font-semibold">Удалить комментарий?</span>
            </div>
          </template>

          <p class="text-muted">
            Вы уверены, что хотите удалить этот комментарий?
            Это действие нельзя отменить.
          </p>

          <template #footer>
            <div class="flex justify-end gap-2">
              <UButton
                color="neutral"
                variant="ghost"
                @click="cancelDelete"
              >
                Отмена
              </UButton>
              <UButton
                color="error"
                :loading="isSubmitting"
                @click="confirmDelete"
              >
                Удалить
              </UButton>
            </div>
          </template>
        </UCard>
      </template>
    </UModal>
  </div>
</template>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.2s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
