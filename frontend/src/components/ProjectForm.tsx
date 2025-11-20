import type { FormEvent } from "react";
import { useState } from "react";

interface Props {
  onSubmit: (name: string, description?: string) => void;
  loading?: boolean;
}

const ProjectForm = ({ onSubmit, loading }: Props) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!name.trim()) return;
    onSubmit(name.trim(), description.trim() || undefined);
    setName("");
    setDescription("");
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <div className="form-row">
        <label htmlFor="project-name">Nombre del proyecto</label>
        <input
          id="project-name"
          placeholder="Migración, Q4 entregables..."
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div className="form-row">
        <label htmlFor="project-desc">Descripción</label>
        <textarea
          id="project-desc"
          placeholder="Alcance, responsables, restricciones"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      <button type="submit" className="primary" disabled={loading}>
        {loading ? "Creando..." : "Crear proyecto"}
      </button>
    </form>
  );
};

export default ProjectForm;
