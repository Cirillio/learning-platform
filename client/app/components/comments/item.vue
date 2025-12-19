<script setup lang="ts">
import type { Comment } from "~/types";

const props = defineProps<{
  comment: Comment;
  depth?: number;
  maxDepth?: number;
}>();

const emit = defineEmits<{
  (e: "reply", commentId: number): void;
  (e: "edit", comment: Comment): void;
  (e: "delete", commentId: number): void;
  (e: "loadReplies", commentId: number): void;
}>();

const depth = computed(() => props.depth || 0);
const maxDepth = computed(() => props.maxDepth || 3);
const canReply = computed(() => depth.value < maxDepth.value);

const isTeacher = computed(() => props.comment.author.role === "teacher");
const hasReplies = computed(
  () =>
    props.comment.replies_count > 0 || (props.comment.replies?.length ?? 0) > 0
);
const showReplies = ref(false);
const isLoadingReplies = ref(false);

// Форматирование даты
const formatDate = (date: string): string => {
  const d = new Date(date);
  const now = new Date();
  const diff = now.getTime() - d.getTime();

  // Менее минуты
  if (diff < 60000) return "только что";

  // Менее часа
  if (diff < 3600000) {
    const mins = Math.floor(diff / 60000);
    return `${mins} ${pluralize(mins, "минуту", "минуты", "минут")} назад`;
  }

  // Менее суток
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000);
    return `${hours} ${pluralize(hours, "час", "часа", "часов")} назад`;
  }

  // Менее недели
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000);
    return `${days} ${pluralize(days, "день", "дня", "дней")} назад`;
  }

  // Форматируем дату
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "short",
    year: d.getFullYear() !== now.getFullYear() ? "numeric" : undefined,
  }).format(d);
};

// Плюрализация
const pluralize = (
  n: number,
  one: string,
  few: string,
  many: string
): string => {
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return one;
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return few;
  return many;
};

// Полное имя автора
const authorName = computed(() => {
  return (
    props.comment.author_name ||
    `${props.comment.author.first_name} ${props.comment.author.last_name}`.trim() ||
    props.comment.author.username
  );
});

// Переключение показа ответов
const toggleReplies = async () => {
  if (
    !showReplies.value &&
    props.comment.replies_count > 0 &&
    !props.comment.replies?.length
  ) {
    isLoadingReplies.value = true;
    emit("loadReplies", props.comment.id);
    // Ждем немного для загрузки
    await new Promise((resolve) => setTimeout(resolve, 100));
    isLoadingReplies.value = false;
  }
  showReplies.value = !showReplies.value;
};
</script>

<template>
  <div class="comment-item">
    <!-- Основной контент комментария -->
    <UCard
      :class="[
        'transition-all duration-200',
        isTeacher ? 'border-primary/20 bg-primary/5' : '',
      ]"
    >
      <div class="flex gap-3">
        <!-- Аватар -->
        <UAvatar
          :src="comment.author_avatar || undefined"
          :alt="authorName"
          size="sm"
          :class="isTeacher ? 'ring-2 ring-primary/50' : ''"
        />

        <!-- Контент -->
        <div class="flex-1 min-w-0">
          <!-- Header: имя, роль, время -->
          <div class="flex items-center flex-wrap gap-2 mb-2">
            <span class="font-medium text-default truncate">{{
              authorName
            }}</span>

            <!-- Badge роли -->
            <UBadge v-if="isTeacher" color="primary" variant="subtle" size="xs">
              <UIcon name="i-lucide-graduation-cap" class="size-3 mr-1" />
              Преподаватель
            </UBadge>
            <UBadge v-else color="neutral" variant="outline" size="xs">
              Студент
            </UBadge>

            <!-- Время -->
            <span class="text-xs text-muted">{{
              formatDate(comment.created_at)
            }}</span>

            <!-- Индикатор редактирования -->
            <span v-if="comment.is_edited" class="text-xs text-muted italic"
              >(изменено)</span
            >
          </div>

          <!-- Текст комментария -->
          <p class="text-sm text-default whitespace-pre-wrap wrap-break-word">
            {{ comment.text }}
          </p>

          <!-- Actions -->
          <div class="flex items-center gap-2 mt-3">
            <!-- Ответить -->
            <UButton
              v-if="canReply"
              size="xs"
              variant="ghost"
              color="neutral"
              icon="i-lucide-message-circle"
              @click="emit('reply', comment.id)"
            >
              Ответить
            </UButton>

            <!-- Показать/скрыть ответы -->
            <UButton
              v-if="hasReplies"
              size="xs"
              variant="ghost"
              color="neutral"
              :icon="
                showReplies ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'
              "
              :loading="isLoadingReplies"
              @click="toggleReplies"
            >
              {{ showReplies ? "Скрыть" : "Показать" }}
              {{ comment.replies_count || comment.replies?.length || 0 }}
              {{
                pluralize(
                  comment.replies_count || comment.replies?.length || 0,
                  "ответ",
                  "ответа",
                  "ответов"
                )
              }}
            </UButton>

            <!-- Spacer -->
            <div class="flex-1" />

            <!-- Редактировать (только автор) -->
            <UButton
              v-if="comment.is_author"
              size="xs"
              variant="ghost"
              color="neutral"
              icon="i-lucide-pencil"
              @click="emit('edit', comment)"
            />

            <!-- Удалить (только автор) -->
            <UButton
              v-if="comment.is_author"
              size="xs"
              variant="ghost"
              color="error"
              icon="i-lucide-trash-2"
              @click="emit('delete', comment.id)"
            />
          </div>
        </div>
      </div>
    </UCard>

    <!-- Вложенные ответы -->
    <Transition name="slide-fade">
      <div
        v-if="showReplies && comment.replies?.length"
        class="ml-6 mt-3 pl-4 border-l-2 border-muted/30 space-y-3"
      >
        <CommentsItem
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
          :depth="depth + 1"
          :max-depth="maxDepth"
          @reply="emit('reply', $event)"
          @edit="emit('edit', $event)"
          @delete="emit('delete', $event)"
          @load-replies="emit('loadReplies', $event)"
        />
      </div>
    </Transition>
  </div>
</template>

<style scoped>
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
