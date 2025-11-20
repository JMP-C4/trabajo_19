import pytest
from pydantic import ValidationError

from app import schemas
from app.models import TaskStatus


@pytest.mark.unit
def test_task_title_trimmed():
    payload = schemas.TaskCreate(title="  Title  ", project_id=1)
    assert payload.title == "Title"


@pytest.mark.unit
def test_task_priority_bounds():
    with pytest.raises(ValidationError):
        schemas.TaskCreate(title="X", project_id=1, priority=6)


@pytest.mark.unit
def test_project_name_min_length():
    with pytest.raises(ValidationError):
        schemas.ProjectCreate(name="ab")


@pytest.mark.unit
def test_status_enum_values():
    payload = schemas.TaskCreate(title="Task", project_id=1, status=TaskStatus.IN_PROGRESS)
    assert payload.status == TaskStatus.IN_PROGRESS


@pytest.mark.unit
@pytest.mark.parametrize(
    "title",
    ["Valid task", "Another task", "Edge Case Title"],
)
def test_multiple_titles(title):
    payload = schemas.TaskCreate(title=title, project_id=1)
    assert payload.title == title
