// ---------------------------------------------------------------------------
// Submissions & Grades
// ---------------------------------------------------------------------------

export type SubmissionStatus = "pending" | "graded" | "returned";

export interface SubmissionFile {
  id: number;
  file: string;
  file_url: string;
  filename: string;
  file_size: number;
  uploaded_at: string;
}

export interface Submission {
  id: number;
  assignment: number; // ID
  assignment_title: string;
  student: number;
  student_name: string;
  content: string;
  status: SubmissionStatus;
  is_late: boolean;
  files_count: number;
  submitted_at: string;
  updated_at: string;
}

export interface SubmissionDetail extends Submission {
  files: SubmissionFile[];
}

export interface Grade {
  id: number;
  submission: number;
  submission_content: string;
  student_name: string;
  assignment_title: string;
  score: number;
  feedback?: string;
  graded_by: number;
  graded_by_name: string;
  graded_at: string;
  updated_at: string;
}
