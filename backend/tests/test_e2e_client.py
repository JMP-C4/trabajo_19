import os
from uuid import uuid4

import httpx
import pytest

BASE_URL = os.getenv("E2E_BASE_URL")

if not BASE_URL:
    pytest.skip("Skip E2E because E2E_BASE_URL is not set", allow_module_level=True)


def _client():
    return httpx.Client(base_url=BASE_URL, timeout=10)


@pytest.mark.e2e
@pytest.mark.parametrize("suffix", range(5))
def test_create_project_end_to_end(suffix):
    name = f"E2E-{suffix}-{uuid4().hex[:6]}"
    with _client() as client:
        resp = client.post("/projects", json={"name": name, "description": "e2e"})
        assert resp.status_code == 201
        created = resp.json()
        assert created["name"] == name


@pytest.mark.e2e
def test_list_projects_end_to_end():
    with _client() as client:
        resp = client.get("/projects")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


@pytest.mark.e2e
def test_task_lifecycle_end_to_end():
    with _client() as client:
        project = client.post("/projects", json={"name": f"E2E-{uuid4().hex[:5]}"})
        project_id = project.json()["id"]
        task = client.post(
            "/tasks",
            json={"title": "Ship E2E", "project_id": project_id, "priority": 2},
        )
        assert task.status_code == 201
        task_id = task.json()["id"]

        updated = client.put(f"/tasks/{task_id}", json={"status": "DONE"})
        assert updated.status_code == 200
        assert updated.json()["status"] == "DONE"

        deleted = client.delete(f"/tasks/{task_id}")
        assert deleted.status_code == 204


@pytest.mark.e2e
def test_filter_tasks_end_to_end():
    with _client() as client:
        projects = client.get("/projects").json()
        if not projects:
            proj = client.post("/projects", json={"name": f"E2E-{uuid4().hex[:5]}"})
            projects = [proj.json()]
        project_id = projects[0]["id"]
        client.post("/tasks", json={"title": "Filter me", "project_id": project_id})
        resp = client.get("/tasks", params={"project_id": project_id})
        assert resp.status_code == 200
        assert all(item["project_id"] == project_id for item in resp.json())


@pytest.mark.e2e
def test_delete_project_end_to_end():
    with _client() as client:
        project = client.post("/projects", json={"name": f"E2E-{uuid4().hex[:5]}"})
        project_id = project.json()["id"]
        resp = client.delete(f"/projects/{project_id}")
        assert resp.status_code == 204


@pytest.mark.e2e
def test_create_multiple_tasks_end_to_end():
    with _client() as client:
        project = client.post("/projects", json={"name": f"E2E-{uuid4().hex[:5]}"})
        project_id = project.json()["id"]
        for idx in range(3):
            client.post("/tasks", json={"title": f"Task {idx}", "project_id": project_id})
        tasks = client.get("/tasks", params={"project_id": project_id}).json()
        assert len(tasks) >= 3
