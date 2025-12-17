/**
 * Типы для системы комментариев
 */

import type { BasicUser, UserRole } from "./user";

// ---------------------------------------------------------------------------
// Comment Author (расширенный пользователь с ролью)
// ---------------------------------------------------------------------------

export interface CommentAuthor extends BasicUser {
  role: UserRole;
  avatar?: string;
}

// ---------------------------------------------------------------------------
// Comment
// ---------------------------------------------------------------------------

export interface Comment {
  id: number;
  content_type: number;
  object_id: number;
  author: CommentAuthor;
  author_name: string;
  author_avatar?: string;
  text: string;
  parent: number | null;
  replies_count: number;
  is_author: boolean;
  is_edited: boolean;
  created_at: string;
  updated_at: string;
  // Вложенные ответы (заполняется на фронтенде)
  replies?: Comment[];
}

// ---------------------------------------------------------------------------
// Comment Create/Update DTOs
// ---------------------------------------------------------------------------

export interface CreateCommentDTO {
  content_type: number;
  object_id: number;
  text: string;
  parent?: number | null;
}

export interface UpdateCommentDTO {
  text: string;
}

// ---------------------------------------------------------------------------
// API Response
// ---------------------------------------------------------------------------

export interface CommentsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Comment[];
}

// ---------------------------------------------------------------------------
// Content Types (для Generic Foreign Key)
// ---------------------------------------------------------------------------

export interface ContentType {
  id: number;
  app_label: string;
  model: string;
}
