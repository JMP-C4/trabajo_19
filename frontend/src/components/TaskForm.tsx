import type { FormEvent } from "react";
import { useState } from "react";

interface Props {
  onSubmit: (title: string, priority: number, dueDate?: string) => void;
  disabled?: boolean;
  loading?: boolean;
}

const TaskForm = ({ onSubmit, disabled, loading }: Props) => {
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState(3);
  const [dueDate, setDueDate] = useState("");

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!title.trim() || disabled) return;
    onSubmit(title.trim(), priority, dueDate || undefined);
    setTitle("");
    setDueDate("");
    setPriority(3);
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <div className="form-row">
        <label htmlFor="task-title">Título de la tarea</label>
        <input
          id="task-title"
          placeholder="Diseñar API, construir dashboard..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          disabled={disabled}
        />
      </div>
      <div className="form-row inline">
        <div>
          <label htmlFor="priority">Prioridad</label>
          <input
            id="priority"
            type="number"
            min={1}
            max={5}
            value={priority}
            onChange={(e) => setPriority(Number(e.target.value))}
            disabled={disabled}
          />
        </div>
        <div>
          <label htmlFor="due-date">Fecha límite</label>
          <input
            id="due-date"
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            disabled={disabled}
          />
        </div>
      </div>
      <button type="submit" className="primary" disabled={disabled || loading}>
        {loading ? "Guardando..." : "Agregar tarea"}
      </button>
      {disabled && <p className="muted">Selecciona un proyecto para agregar tareas.</p>}
    </form>
  );
};

export default TaskForm;
