// ---------------------------------------------------------------------------
// Assignments
// ---------------------------------------------------------------------------

export interface AssignmentFile {
  id: number;
  file: string;
  file_url: string;
  filename: string;
  file_size: number;
  uploaded_at: string;
}

export interface Assignment {
  id: number;
  lesson: string; // slug
  title: string;
  description: string;
  instructions: string;
  max_score: number;
  due_date?: string | null;
  is_required: boolean;
  allow_late_submission: boolean;
  files: AssignmentFile[];
  submissions_count: number;
  // Статус для студента
  is_submitted?: boolean;
  created_at: string;
  updated_at: string;
}
