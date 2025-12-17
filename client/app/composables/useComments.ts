import type { Comment, CreateCommentDTO, UpdateCommentDTO } from "~/types";
import { useCommentsService } from "~/services/useCommentsService";

interface UseCommentsOptions {
  /** ID урока */
  lessonId: number;
  /** ContentType ID для уроков (будет получен автоматически если не указан) */
  contentTypeId?: number;
}

/**
 * Composable для работы с комментариями к уроку
 */
export const useComments = (options: UseCommentsOptions) => {
  const commentsService = useCommentsService();
  const toast = useToast();
  const { user } = useAuth();

  // State
  const comments = ref<Comment[]>([]);
  const totalCount = ref(0);
  const currentPage = ref(1);
  const hasMore = ref(false);

  const isLoading = ref(false);
  const isLoadingMore = ref(false);
  const isSubmitting = ref(false);
  const error = ref<Error | null>(null);

  // ContentType ID для уроков (кэшируется)
  const contentTypeId = ref<number>(options.contentTypeId || 0);

  // Computed
  const isEmpty = computed(() => comments.value.length === 0 && !isLoading.value);
  const canLoadMore = computed(() => hasMore.value && !isLoadingMore.value);

  /**
   * Инициализация: получение ContentType ID если не указан
   */
  const initContentType = async () => {
    if (contentTypeId.value === 0) {
      contentTypeId.value = await commentsService.getLessonContentType();
    }
  };

  /**
   * Построение дерева комментариев из плоского списка
   */
  const buildCommentsTree = (flatComments: Comment[]): Comment[] => {
    const commentMap = new Map<number, Comment>();
    const rootComments: Comment[] = [];

    // Создаем карту комментариев
    flatComments.forEach((comment) => {
      commentMap.set(comment.id, { ...comment, replies: [] });
    });

    // Строим дерево
    flatComments.forEach((comment) => {
      const node = commentMap.get(comment.id)!;
      if (comment.parent) {
        const parent = commentMap.get(comment.parent);
        if (parent) {
          parent.replies = parent.replies || [];
          parent.replies.push(node);
        } else {
          // Родитель не найден, добавляем как корневой
          rootComments.push(node);
        }
      } else {
        rootComments.push(node);
      }
    });

    return rootComments;
  };

  /**
   * Загрузка комментариев
   */
  const fetchComments = async (page = 1) => {
    if (page === 1) {
      isLoading.value = true;
    } else {
      isLoadingMore.value = true;
    }
    error.value = null;

    try {
      await initContentType();

      const response = await commentsService.getComments({
        content_type: contentTypeId.value,
        object_id: options.lessonId,
        page,
        page_size: 20,
      });

      const newComments = response.results;

      if (page === 1) {
        comments.value = newComments;
      } else {
        // Добавляем новые комментарии, избегая дубликатов
        const existingIds = new Set(comments.value.map((c) => c.id));
        const uniqueNew = newComments.filter((c) => !existingIds.has(c.id));
        comments.value = [...comments.value, ...uniqueNew];
      }

      totalCount.value = response.count;
      currentPage.value = page;
      hasMore.value = response.next !== null;
    } catch (e) {
      error.value = e as Error;
      console.error("Failed to fetch comments:", e);
      toast.add({
        title: "Ошибка",
        description: "Не удалось загрузить комментарии",
        color: "error",
      });
    } finally {
      isLoading.value = false;
      isLoadingMore.value = false;
    }
  };

  /**
   * Загрузка следующей страницы
   */
  const loadMore = () => {
    if (canLoadMore.value) {
      fetchComments(currentPage.value + 1);
    }
  };

  /**
   * Добавление комментария (с optimistic update)
   */
  const addComment = async (text: string, parentId?: number | null) => {
    if (!user.value) {
      toast.add({
        title: "Ошибка",
        description: "Необходимо авторизоваться",
        color: "error",
      });
      return null;
    }

    isSubmitting.value = true;
    error.value = null;

    // Optimistic update - создаем временный комментарий
    const tempId = Date.now();
    const tempComment: Comment = {
      id: tempId,
      content_type: contentTypeId.value,
      object_id: options.lessonId,
      author: {
        id: user.value.id,
        username: user.value.username,
        first_name: user.value.first_name,
        last_name: user.value.last_name,
        role: user.value.role,
        avatar: user.value.avatar || undefined,
      },
      author_name: `${user.value.first_name} ${user.value.last_name}`.trim() || user.value.username,
      author_avatar: user.value.avatar || undefined,
      text,
      parent: parentId || null,
      replies_count: 0,
      is_author: true,
      is_edited: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      replies: [],
    };

    // Добавляем временный комментарий
    if (parentId) {
      // Добавляем как ответ
      addReplyToComment(comments.value, parentId, tempComment);
    } else {
      // Добавляем в начало списка
      comments.value = [tempComment, ...comments.value];
    }

    try {
      await initContentType();

      const payload: CreateCommentDTO = {
        content_type: contentTypeId.value,
        object_id: options.lessonId,
        text,
        parent: parentId || null,
      };

      const newComment = await commentsService.createComment(payload);

      // Заменяем временный комментарий реальным
      replaceComment(comments.value, tempId, { ...newComment, replies: [] });
      totalCount.value++;

      toast.add({
        title: "Комментарий добавлен",
        color: "success",
      });

      return newComment;
    } catch (e) {
      // Откатываем optimistic update
      removeComment(comments.value, tempId);

      error.value = e as Error;
      console.error("Failed to create comment:", e);
      toast.add({
        title: "Ошибка",
        description: "Не удалось добавить комментарий",
        color: "error",
      });
      return null;
    } finally {
      isSubmitting.value = false;
    }
  };

  /**
   * Обновление комментария
   */
  const updateComment = async (commentId: number, text: string) => {
    isSubmitting.value = true;
    error.value = null;

    // Сохраняем старый текст для отката
    const oldComment = findComment(comments.value, commentId);
    const oldText = oldComment?.text;

    // Optimistic update
    if (oldComment) {
      oldComment.text = text;
      oldComment.is_edited = true;
      oldComment.updated_at = new Date().toISOString();
    }

    try {
      const payload: UpdateCommentDTO = { text };
      const updated = await commentsService.updateComment(commentId, payload);

      // Обновляем комментарий реальными данными
      replaceComment(comments.value, commentId, { ...updated, replies: oldComment?.replies || [] });

      toast.add({
        title: "Комментарий обновлён",
        color: "success",
      });

      return updated;
    } catch (e) {
      // Откатываем optimistic update
      if (oldComment && oldText) {
        oldComment.text = oldText;
        oldComment.is_edited = false;
      }

      error.value = e as Error;
      console.error("Failed to update comment:", e);
      toast.add({
        title: "Ошибка",
        description: "Не удалось обновить комментарий",
        color: "error",
      });
      return null;
    } finally {
      isSubmitting.value = false;
    }
  };

  /**
   * Удаление комментария
   */
  const deleteComment = async (commentId: number) => {
    isSubmitting.value = true;
    error.value = null;

    // Сохраняем для возможного отката
    const deletedComment = findComment(comments.value, commentId);
    const parentId = deletedComment?.parent;

    // Optimistic update
    removeComment(comments.value, commentId);
    totalCount.value--;

    try {
      await commentsService.deleteComment(commentId);

      toast.add({
        title: "Комментарий удалён",
        color: "success",
      });

      return true;
    } catch (e) {
      // Откатываем optimistic update
      if (deletedComment) {
        if (parentId) {
          addReplyToComment(comments.value, parentId, deletedComment);
        } else {
          comments.value.push(deletedComment);
        }
        totalCount.value++;
      }

      error.value = e as Error;
      console.error("Failed to delete comment:", e);
      toast.add({
        title: "Ошибка",
        description: "Не удалось удалить комментарий",
        color: "error",
      });
      return false;
    } finally {
      isSubmitting.value = false;
    }
  };

  /**
   * Загрузка ответов на комментарий
   */
  const loadReplies = async (commentId: number) => {
    try {
      const response = await commentsService.getReplies(commentId);
      const comment = findComment(comments.value, commentId);

      if (comment) {
        comment.replies = response.results.map((r) => ({ ...r, replies: [] }));
      }

      return response.results;
    } catch (e) {
      console.error("Failed to load replies:", e);
      toast.add({
        title: "Ошибка",
        description: "Не удалось загрузить ответы",
        color: "error",
      });
      return [];
    }
  };

  // Helper functions for tree manipulation
  const findComment = (list: Comment[], id: number): Comment | null => {
    for (const comment of list) {
      if (comment.id === id) return comment;
      if (comment.replies?.length) {
        const found = findComment(comment.replies, id);
        if (found) return found;
      }
    }
    return null;
  };

  const replaceComment = (list: Comment[], id: number, newComment: Comment) => {
    for (let i = 0; i < list.length; i++) {
      const item = list[i];
      if (!item) continue;
      if (item.id === id) {
        list[i] = newComment;
        return true;
      }
      if (item.replies?.length) {
        if (replaceComment(item.replies, id, newComment)) return true;
      }
    }
    return false;
  };

  const removeComment = (list: Comment[], id: number): boolean => {
    for (let i = 0; i < list.length; i++) {
      const item = list[i];
      if (!item) continue;
      if (item.id === id) {
        list.splice(i, 1);
        return true;
      }
      if (item.replies?.length) {
        if (removeComment(item.replies, id)) return true;
      }
    }
    return false;
  };

  const addReplyToComment = (list: Comment[], parentId: number, reply: Comment) => {
    for (const comment of list) {
      if (comment.id === parentId) {
        comment.replies = comment.replies || [];
        comment.replies.push(reply);
        comment.replies_count++;
        return true;
      }
      if (comment.replies?.length) {
        if (addReplyToComment(comment.replies, parentId, reply)) return true;
      }
    }
    return false;
  };

  /**
   * Обновление при смене урока
   */
  const reset = () => {
    comments.value = [];
    totalCount.value = 0;
    currentPage.value = 1;
    hasMore.value = false;
    error.value = null;
  };

  // Watch для автоматической загрузки при изменении lessonId
  watch(
    () => options.lessonId,
    (newId, oldId) => {
      if (newId !== oldId && newId > 0) {
        reset();
        fetchComments();
      }
    },
    { immediate: false }
  );

  return {
    // State
    comments,
    totalCount: readonly(totalCount),
    currentPage: readonly(currentPage),
    hasMore: readonly(hasMore),
    isLoading: readonly(isLoading),
    isLoadingMore: readonly(isLoadingMore),
    isSubmitting: readonly(isSubmitting),
    error: readonly(error),

    // Computed
    isEmpty,
    canLoadMore,

    // Actions
    fetchComments,
    loadMore,
    addComment,
    updateComment,
    deleteComment,
    loadReplies,
    reset,
  };
};
