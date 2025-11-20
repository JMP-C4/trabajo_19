import pytest

from app import crud, schemas


@pytest.mark.benchmark
def test_list_tasks_performance(db_session, benchmark):
    project = crud.create_project(db_session, schemas.ProjectCreate(name="Bench"))
    for i in range(50):
        crud.create_task(db_session, schemas.TaskCreate(title=f"Task {i}", project_id=project.id))

    def run_query():
        return crud.list_tasks(db_session)

    result = benchmark(run_query)
    assert len(result) == 50


@pytest.mark.benchmark
def test_create_task_performance(db_session, benchmark):
    project = crud.create_project(db_session, schemas.ProjectCreate(name="Bench2"))

    def create_task():
        return crud.create_task(
            db_session,
            schemas.TaskCreate(title="Bench task", project_id=project.id),
        )

    task = benchmark(create_task)
    assert task.project_id == project.id


@pytest.mark.benchmark
def test_update_task_performance(db_session, benchmark):
    project = crud.create_project(db_session, schemas.ProjectCreate(name="Bench3"))
    task = crud.create_task(db_session, schemas.TaskCreate(title="To update", project_id=project.id))

    def update_task():
        return crud.update_task(
            db_session,
            task.id,
            schemas.TaskUpdate(title="Updated title"),
        )

    updated = benchmark(update_task)
    assert updated.title == "Updated title"


@pytest.mark.benchmark
def test_filter_tasks_performance(db_session, benchmark):
    project = crud.create_project(db_session, schemas.ProjectCreate(name="Bench4"))
    for i in range(20):
        crud.create_task(db_session, schemas.TaskCreate(title=f"Bench {i}", project_id=project.id))

    def filter_tasks():
        return crud.list_tasks(db_session, project_id=project.id)

    tasks = benchmark(filter_tasks)
    assert len(tasks) == 20


@pytest.mark.benchmark
def test_delete_task_performance(db_session, benchmark):
    project = crud.create_project(db_session, schemas.ProjectCreate(name="Bench5"))
    task = crud.create_task(db_session, schemas.TaskCreate(title="Delete me", project_id=project.id))

    def delete_task():
        crud.delete_task(db_session, task.id)
        return True

    assert benchmark(delete_task)
