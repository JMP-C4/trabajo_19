import type { Task } from "../types";

interface Props {
  tasks: Task[];
}

const Metrics = ({ tasks }: Props) => {
  const todo = tasks.filter((t) => t.status === "TODO").length;
  const inProgress = tasks.filter((t) => t.status === "IN_PROGRESS").length;
  const done = tasks.filter((t) => t.status === "DONE").length;

  return (
    <div className="metrics">
      <div className="metric-card">
        <p className="eyebrow">Pendientes</p>
        <h3>{todo}</h3>
      </div>
      <div className="metric-card">
        <p className="eyebrow">En curso</p>
        <h3>{inProgress}</h3>
      </div>
      <div className="metric-card">
        <p className="eyebrow">Completadas</p>
        <h3>{done}</h3>
      </div>
    </div>
  );
};

export default Metrics;
