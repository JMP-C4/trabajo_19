import pytest


def _create_project(client, name="Core", description="desc"):
    response = client.post("/projects", json={"name": name, "description": description})
    assert response.status_code == 201
    return response.json()


def _create_task(client, project_id: int, title="Task", status="TODO", priority=3):
    payload = {
        "title": title,
        "project_id": project_id,
        "status": status,
        "priority": priority,
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


@pytest.mark.integration
@pytest.mark.parametrize("name", ["Ops", "Product", "Engineering", "QA"])
def test_create_projects(client, name):
    response = client.post("/projects", json={"name": name, "description": f"{name} desc"})
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == name


@pytest.mark.integration
def test_duplicate_project_conflict(client):
    client.post("/projects", json={"name": "Duplicate", "description": "First"})
    response = client.post("/projects", json={"name": "Duplicate", "description": "Second"})
    assert response.status_code == 409


@pytest.mark.integration
def test_get_project_by_id(client):
    created = _create_project(client, "GetMe")
    response = client.get(f"/projects/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "GetMe"


@pytest.mark.integration
def test_update_project_fields(client):
    created = _create_project(client, "OldName")
    response = client.put(f"/projects/{created['id']}", json={"name": "NewName"})
    assert response.status_code == 200
    assert response.json()["name"] == "NewName"


@pytest.mark.integration
def test_delete_project_removes_tasks(client):
    project = _create_project(client, "Remove")
    _create_task(client, project["id"], "A")
    response = client.delete(f"/projects/{project['id']}")
    assert response.status_code == 204
    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    assert list_response.json() == []


@pytest.mark.integration
@pytest.mark.parametrize(
    "status",
    ["TODO", "IN_PROGRESS", "DONE"],
)
def test_create_task_for_project(client, status):
    project = _create_project(client, "Tasks")
    task = _create_task(client, project["id"], status=status, title=f"{status} task")
    assert task["status"] == status


@pytest.mark.integration
@pytest.mark.parametrize(
    "new_status",
    ["IN_PROGRESS", "DONE", "TODO"],
)
def test_update_task_status(client, new_status):
    project = _create_project(client, "Pipeline")
    task = _create_task(client, project["id"], status="TODO")
    response = client.put(f"/tasks/{task['id']}", json={"status": new_status})
    assert response.status_code == 200
    assert response.json()["status"] == new_status


@pytest.mark.integration
def test_list_tasks_filtering(client):
    project_a = _create_project(client, "A")
    project_b = _create_project(client, "B")
    _create_task(client, project_a["id"], "A1")
    _create_task(client, project_b["id"], "B1")

    response = client.get("/tasks", params={"project_id": project_a["id"]})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["project"]["name"] == "A"


@pytest.mark.integration
def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404


@pytest.mark.integration
def test_delete_task(client):
    project = _create_project(client, "Cleaner")
    task = _create_task(client, project["id"], "Temp")
    response = client.delete(f"/tasks/{task['id']}")
    assert response.status_code == 204


@pytest.mark.integration
@pytest.mark.parametrize("priority", [1, 2, 3])
def test_task_priority_persistence(client, priority):
    project = _create_project(client, "Priorities")
    task = _create_task(client, project["id"], title=f"P{priority}", priority=priority)
    assert task["priority"] == priority
