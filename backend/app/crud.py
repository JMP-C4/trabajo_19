"""CRUD layer for projects and tasks."""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from . import models, schemas


def create_project(db: Session, project_in: schemas.ProjectCreate) -> models.Project:
    project = models.Project(**project_in.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session) -> List[models.Project]:
    return db.execute(select(models.Project).order_by(models.Project.created_at.desc())).scalars().all()


def get_project(db: Session, project_id: int) -> models.Project:
    project = db.get(models.Project, project_id)
    if not project:
        raise NoResultFound(f"Project {project_id} not found")
    return project


def update_project(db: Session, project_id: int, project_in: schemas.ProjectUpdate) -> models.Project:
    project = get_project(db, project_id)
    for field, value in project_in.dict(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int) -> None:
    project = get_project(db, project_id)
    db.delete(project)
    db.commit()


def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    _ensure_project_exists(db, task_in.project_id)
    task = models.Task(**task_in.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session, project_id: Optional[int] = None) -> List[models.Task]:
    stmt = select(models.Task).order_by(models.Task.created_at.desc())
    if project_id:
        stmt = stmt.where(models.Task.project_id == project_id)
    return db.execute(stmt).scalars().all()


def get_task(db: Session, task_id: int) -> models.Task:
    task = db.get(models.Task, task_id)
    if not task:
        raise NoResultFound(f"Task {task_id} not found")
    return task


def update_task(db: Session, task_id: int, task_in: schemas.TaskUpdate) -> models.Task:
    task = get_task(db, task_id)
    data = task_in.dict(exclude_unset=True)
    if "project_id" in data:
        _ensure_project_exists(db, data["project_id"])
    for field, value in data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> None:
    task = get_task(db, task_id)
    db.delete(task)
    db.commit()


def _ensure_project_exists(db: Session, project_id: int) -> None:
    if not db.get(models.Project, project_id):
        raise NoResultFound(f"Project {project_id} not found")
