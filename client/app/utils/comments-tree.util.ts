import type { Comment } from "~/types";

/**
 * Рекурсивный поиск комментария в дереве
 */
export const findComment = (list: Comment[], id: number): Comment | null => {
  for (const comment of list) {
    if (comment.id === id) return comment;
    if (comment.replies?.length) {
      const found = findComment(comment.replies, id);
      if (found) return found;
    }
  }
  return null;
};

/**
 * Рекурсивная замена комментария в дереве
 */
export const replaceComment = (
  list: Comment[],
  id: number,
  newComment: Comment
): boolean => {
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

/**
 * Рекурсивное удаление комментария из дерева
 */
export const removeComment = (list: Comment[], id: number): boolean => {
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

/**
 * Добавление ответа к комментарию
 */
export const addReplyToComment = (
  list: Comment[],
  parentId: number,
  reply: Comment
): boolean => {
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
