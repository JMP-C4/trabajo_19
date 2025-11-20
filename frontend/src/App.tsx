import { useEffect, useMemo, useState } from "react";

import Header from "./components/Header";
import Metrics from "./components/Metrics";
import ProjectForm from "./components/ProjectForm";
import ProjectList from "./components/ProjectList";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import { createProject, fetchProjects } from "./store/projectsSlice";
import {
  createTask,
  deleteTask,
  fetchTasks,
  setFilterProject,
  updateTaskStatus,
} from "./store/tasksSlice";
import { useAppDispatch, useAppSelector } from "./store";
import type { TaskStatus } from "./types";

const App = () => {
  const dispatch = useAppDispatch();
  const { items: projects, status: projectsStatus } = useAppSelector((state) => state.projects);
  const { items: tasks, status: tasksStatus } = useAppSelector((state) => state.tasks);
  const [selectedProject, setSelectedProject] = useState<number | undefined>(undefined);

  useEffect(() => {
    dispatch(fetchProjects());
  }, [dispatch]);

  useEffect(() => {
    if (!selectedProject && projects.length) {
      setSelectedProject(projects[0].id);
    }
  }, [projects, selectedProject]);

  useEffect(() => {
    dispatch(fetchTasks(selectedProject));
    dispatch(setFilterProject(selectedProject));
  }, [dispatch, selectedProject]);

  const handleCreateProject = (name: string, description?: string) => {
    dispatch(createProject({ name, description }));
  };

  const handleCreateTask = (title: string, priority: number, dueDate?: string) => {
    if (!selectedProject) return;
    dispatch(createTask({ title, project_id: selectedProject, priority, due_date: dueDate }));
  };

  const handleAdvanceStatus = (taskId: number, currentStatus: TaskStatus) => {
    const order: TaskStatus[] = ["TODO", "IN_PROGRESS", "DONE"];
    const next = order[(order.indexOf(currentStatus) + 1) % order.length];
    dispatch(updateTaskStatus({ id: taskId, status: next }));
  };

  const handleDeleteTask = (taskId: number) => {
    dispatch(deleteTask(taskId));
  };

  const filteredTasks = useMemo(() => {
    if (!selectedProject) return tasks;
    return tasks.filter((task) => task.project_id === selectedProject);
  }, [tasks, selectedProject]);

  return (
    <div className="page">
      <Header />
      <main className="content">
        <section className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Proyectos</p>
              <h2>Organiza los flujos de trabajo</h2>
            </div>
            <span className="pill">{projects.length} activos</span>
          </div>
          <ProjectForm onSubmit={handleCreateProject} loading={projectsStatus === "loading"} />
          <ProjectList
            projects={projects}
            selectedProjectId={selectedProject}
            onSelect={setSelectedProject}
          />
        </section>

        <section className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Tareas</p>
              <h2>Entregables</h2>
            </div>
            <span className="pill">{filteredTasks.length} tareas</span>
          </div>
          <TaskForm
            disabled={!selectedProject}
            onSubmit={handleCreateTask}
            loading={tasksStatus === "loading"}
          />
          <TaskList
            tasks={filteredTasks}
            onAdvanceStatus={handleAdvanceStatus}
            onDelete={handleDeleteTask}
          />
        </section>

        <section className="panel">
          <Metrics tasks={tasks} />
        </section>
      </main>
    </div>
  );
};

export default App;
