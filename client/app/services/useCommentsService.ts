import type {
  Comment,
  CommentsResponse,
  CreateCommentDTO,
  UpdateCommentDTO,
  ContentType,
} from "~/types";

interface CommentsFilters {
  content_type?: number;
  object_id?: number;
  parent?: number;
  top_level?: boolean;
  page?: number;
  page_size?: number;
}

/**
 * Service для работы с комментариями
 */
export const useCommentsService = () => {
  const api = useApi();

  /**
   * Получить список комментариев
   * @param filters - Фильтры для запроса
   */
  const getComments = (filters?: CommentsFilters) => {
    const params: Record<string, string | number | boolean> = {};

    if (filters?.content_type) params.content_type = filters.content_type;
    if (filters?.object_id) params.object_id = filters.object_id;
    if (filters?.parent) params.parent = filters.parent;
    if (filters?.top_level) params.top_level = "true";
    if (filters?.page) params.page = filters.page;
    if (filters?.page_size) params.page_size = filters.page_size;

    return api.get<CommentsResponse>("/core/comments/", params);
  };

  /**
   * Получить комментарий по ID
   */
  const getComment = (id: number) => {
    return api.get<Comment>(`/core/comments/${id}/`);
  };

  /**
   * Создать комментарий
   */
  const createComment = (payload: CreateCommentDTO) => {
    return api.post<Comment>("/core/comments/", payload);
  };

  /**
   * Обновить комментарий
   */
  const updateComment = (id: number, payload: UpdateCommentDTO) => {
    return api.patch<Comment>(`/core/comments/${id}/`, payload);
  };

  /**
   * Удалить комментарий
   */
  const deleteComment = (id: number) => {
    return api.delete<void>(`/core/comments/${id}/`);
  };

  /**
   * Получить ответы на комментарий
   */
  const getReplies = (commentId: number, page = 1) => {
    return api.get<CommentsResponse>("/core/comments/", {
      parent: commentId,
      page,
    });
  };

  /**
   * Получить ContentType для модели Lesson
   * Кэшируем результат, так как он не меняется
   */
  let lessonContentTypeId: number | null = null;

  const getLessonContentType = async (): Promise<number> => {
    if (lessonContentTypeId !== null) {
      return lessonContentTypeId;
    }

    // Получаем ContentType ID для модели Lesson
    // Это нужно для Generic Foreign Key в комментариях
    try {
      const response = await api.get<ContentType[]>("/core/content-types/", {
        app_label: "courses",
        model: "lesson",
      });

      if (response && response.length > 0 && response[0]) {
        lessonContentTypeId = response[0].id;
        return lessonContentTypeId;
      }
    } catch {
      // Если эндпоинт недоступен, используем хардкод (нужно будет настроить на бэкенде)
      console.warn("ContentType endpoint not available, using hardcoded value");
    }

    // Fallback значение (нужно обновить на реальный ID из базы)
    return 0;
  };

  return {
    getComments,
    getComment,
    createComment,
    updateComment,
    deleteComment,
    getReplies,
    getLessonContentType,
  };
};
