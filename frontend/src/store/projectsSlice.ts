import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

import { api } from "../api";
import type { Project } from "../types";

export interface ProjectInput {
  name: string;
  description?: string;
}

interface ProjectsState {
  items: Project[];
  status: "idle" | "loading" | "failed";
  error?: string;
}

const initialState: ProjectsState = {
  items: [],
  status: "idle",
};

export const fetchProjects = createAsyncThunk("projects/fetch", async () => {
  const { data } = await api.get<Project[]>("/projects");
  return data;
});

export const createProject = createAsyncThunk("projects/create", async (payload: ProjectInput) => {
  const { data } = await api.post<Project>("/projects", payload);
  return data;
});

export const deleteProject = createAsyncThunk("projects/delete", async (projectId: number) => {
  await api.delete(`/projects/${projectId}`);
  return projectId;
});

const projectsSlice = createSlice({
  name: "projects",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchProjects.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchProjects.fulfilled, (state, action: PayloadAction<Project[]>) => {
        state.status = "idle";
        state.items = action.payload;
      })
      .addCase(fetchProjects.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
      })
      .addCase(createProject.fulfilled, (state, action: PayloadAction<Project>) => {
        state.items.unshift(action.payload);
      })
      .addCase(deleteProject.fulfilled, (state, action: PayloadAction<number>) => {
        state.items = state.items.filter((item) => item.id !== action.payload);
      });
  },
});

export default projectsSlice.reducer;
