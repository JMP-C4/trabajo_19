import type { Project } from "../types";

interface Props {
  projects: Project[];
  selectedProjectId?: number;
  onSelect: (id?: number) => void;
}

const ProjectList = ({ projects, selectedProjectId, onSelect }: Props) => {
  if (!projects.length) {
    return <p className="muted">Aún no hay proyectos. Crea uno para empezar a planificar.</p>;
  }

  return (
    <div className="grid two-col">
      {projects.map((project) => (
        <button
          type="button"
          key={project.id}
          className={`card ${selectedProjectId === project.id ? "card-active" : ""}`}
          onClick={() => onSelect(project.id)}
        >
          <div className="card-header">
            <h3>{project.name}</h3>
            <span className="pill subtle">#{project.id}</span>
          </div>
          <p className="muted">{project.description || "Sin descripción."}</p>
        </button>
      ))}
    </div>
  );
};

export default ProjectList;
