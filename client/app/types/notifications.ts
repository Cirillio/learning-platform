import type { BasicUser } from "./user";

// ---------------------------------------------------------------------------
// Notifications
// ---------------------------------------------------------------------------

export interface Notification {
  id: number;
  recipient: BasicUser;
  notification_type: string; // 'assignment_deadline', 'grade_received', etc.
  title: string;
  message: string;
  content_type: number | null;
  object_id: number | null;
  is_read: boolean;
  read_at?: string | null;
  created_at: string;
  email_sent: boolean;
  email_sent_at?: string | null;
}
