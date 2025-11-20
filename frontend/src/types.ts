export type TaskStatus = "TODO" | "IN_PROGRESS" | "DONE";

export interface Project {
  id: number;
  name: string;
  description?: string | null;
  created_at?: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string | null;
  status: TaskStatus;
  priority: number;
  due_date?: string | null;
  project_id: number;
  project?: Project;
  created_at?: string;
  updated_at?: string;
}
