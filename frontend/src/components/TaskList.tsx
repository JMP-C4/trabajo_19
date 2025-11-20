import type { Task, TaskStatus } from "../types";

interface Props {
  tasks: Task[];
  onAdvanceStatus: (taskId: number, currentStatus: TaskStatus) => void;
  onDelete: (taskId: number) => void;
}

const statusColor: Record<TaskStatus, string> = {
  TODO: "muted",
  IN_PROGRESS: "warning",
  DONE: "success",
};

const columns: Array<{ key: TaskStatus; title: string; hint: string }> = [
  { key: "TODO", title: "Por hacer", hint: "Define alcance" },
  { key: "IN_PROGRESS", title: "En progreso", hint: "Ejecutando" },
  { key: "DONE", title: "Completadas", hint: "Cerradas" },
];

const TaskList = ({ tasks, onAdvanceStatus, onDelete }: Props) => (
  <div className="board">
    {columns.map((column) => {
      const items = tasks.filter((task) => task.status === column.key);
      return (
        <div key={column.key} className="column">
          <div className="column-header">
            <div>
              <p className="eyebrow">{column.hint}</p>
              <h3>{column.title}</h3>
            </div>
            <span className={`pill ${statusColor[column.key]}`}>{items.length}</span>
          </div>
          {items.length === 0 ? (
            <p className="muted small">Nada aquí todavía.</p>
          ) : (
            <div className="column-list">
              {items.map((task) => (
                <div key={task.id} className="card task-card">
                  <div className="card-header">
                    <span className="pill subtle">#{task.id}</span>
                    <span className="pill subtle">P{task.priority}</span>
                  </div>
                  <h4>{task.title}</h4>
                  <p className="muted">Proyecto: {task.project?.name ?? task.project_id}</p>
                  <div className="row gap">
                    <button
                      type="button"
                      className="ghost"
                      onClick={() => onAdvanceStatus(task.id, task.status)}
                    >
                      Avanzar
                    </button>
                    <button type="button" className="ghost danger" onClick={() => onDelete(task.id)}>
                      Eliminar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      );
    })}
  </div>
);

export default TaskList;
