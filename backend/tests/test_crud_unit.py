import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import crud, schemas
from app.database import Base
from app.models import TaskStatus


@pytest.fixture
def sqlite_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.mark.unit
def test_create_project(sqlite_session):
    project = crud.create_project(sqlite_session, schemas.ProjectCreate(name="Ops", description="DevOps"))
    assert project.id == 1
    assert project.name == "Ops"


@pytest.mark.unit
def test_create_task(sqlite_session):
    project = crud.create_project(sqlite_session, schemas.ProjectCreate(name="Web", description=None))
    task = crud.create_task(
        sqlite_session,
        schemas.TaskCreate(title="Build UI", project_id=project.id, priority=2, status=TaskStatus.TODO),
    )
    assert task.project_id == project.id
    assert task.status == TaskStatus.TODO


@pytest.mark.unit
def test_update_task_status(sqlite_session):
    project = crud.create_project(sqlite_session, schemas.ProjectCreate(name="API"))
    task = crud.create_task(sqlite_session, schemas.TaskCreate(title="Implement", project_id=project.id))
    updated = crud.update_task(
        sqlite_session,
        task.id,
        schemas.TaskUpdate(status=TaskStatus.DONE, title="Implement Done"),
    )
    assert updated.status == TaskStatus.DONE
    assert updated.title == "Implement Done"


@pytest.mark.unit
def test_list_tasks_filters_by_project(sqlite_session):
    project_a = crud.create_project(sqlite_session, schemas.ProjectCreate(name="A"))
    project_b = crud.create_project(sqlite_session, schemas.ProjectCreate(name="B"))
    crud.create_task(sqlite_session, schemas.TaskCreate(title="Task A1", project_id=project_a.id))
    crud.create_task(sqlite_session, schemas.TaskCreate(title="Task B1", project_id=project_b.id))

    tasks_a = crud.list_tasks(sqlite_session, project_id=project_a.id)
    assert len(tasks_a) == 1
    assert tasks_a[0].project_id == project_a.id


@pytest.mark.unit
def test_delete_project_cascades(sqlite_session):
    project = crud.create_project(sqlite_session, schemas.ProjectCreate(name="OpsProject"))
    crud.create_task(sqlite_session, schemas.TaskCreate(title="Task 1", project_id=project.id))
    crud.delete_project(sqlite_session, project.id)
    assert crud.list_tasks(sqlite_session) == []
