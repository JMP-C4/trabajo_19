import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

import { api } from "../api";
import type { Task, TaskStatus } from "../types";

export interface TaskInput {
  title: string;
  description?: string;
  status?: TaskStatus;
  priority?: number;
  due_date?: string | null;
  project_id: number;
}

interface TasksState {
  items: Task[];
  status: "idle" | "loading" | "failed";
  error?: string;
  filterProjectId?: number;
}

const initialState: TasksState = {
  items: [],
  status: "idle",
};

export const fetchTasks = createAsyncThunk("tasks/fetch", async (projectId?: number) => {
  const { data } = await api.get<Task[]>("/tasks", { params: projectId ? { project_id: projectId } : {} });
  return data;
});

export const createTask = createAsyncThunk("tasks/create", async (payload: TaskInput) => {
  const { data } = await api.post<Task>("/tasks", payload);
  return data;
});

export const updateTaskStatus = createAsyncThunk(
  "tasks/updateStatus",
  async ({ id, status }: { id: number; status: TaskStatus }) => {
    const { data } = await api.put<Task>(`/tasks/${id}`, { status });
    return data;
  },
);

export const deleteTask = createAsyncThunk("tasks/delete", async (taskId: number) => {
  await api.delete(`/tasks/${taskId}`);
  return taskId;
});

const tasksSlice = createSlice({
  name: "tasks",
  initialState,
  reducers: {
    setFilterProject(state, action: PayloadAction<number | undefined>) {
      state.filterProjectId = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTasks.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchTasks.fulfilled, (state, action: PayloadAction<Task[]>) => {
        state.status = "idle";
        state.items = action.payload;
      })
      .addCase(fetchTasks.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
      })
      .addCase(createTask.fulfilled, (state, action: PayloadAction<Task>) => {
        state.items.unshift(action.payload);
      })
      .addCase(updateTaskStatus.fulfilled, (state, action: PayloadAction<Task>) => {
        const idx = state.items.findIndex((t) => t.id === action.payload.id);
        if (idx >= 0) {
          state.items[idx] = action.payload;
        }
      })
      .addCase(deleteTask.fulfilled, (state, action: PayloadAction<number>) => {
        state.items = state.items.filter((t) => t.id != action.payload);
      });
  },
});

export const { setFilterProject } = tasksSlice.actions;
export default tasksSlice.reducer;
