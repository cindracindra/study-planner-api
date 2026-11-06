from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_CONTENT,
)
from freezegun import freeze_time

from tests.conftest import HPOTTER_CREDENTIALS


def test_tasks_endpoint_returns_200(client, task_factory):
    task_factory.create(username="hpotter", year="2526")
    res = client.get("me/2526/personal-tasks", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_200_OK


def test_tasks_response_contains_expected_fields(client, task_factory):
    task_factory.create(username="hpotter", year="2526")
    res = client.get("me/2526/personal-tasks", auth=HPOTTER_CREDENTIALS)
    task = res.json()[0]
    expected_fields = {
        "id",
        "year",
        "username",
        "title",
        "creation_date",
        "task_completed",
    }
    assert expected_fields.issubset(task.keys())


def test_tasks_response_only_contains_tasks_for_user_and_year(client, task_factory):
    task_factory.create(username="hpotter", year="2425")
    task_factory.create(username="hgranger", year="2425")
    task_factory.create(username="hpotter", year="2526")
    task_factory.create(username="hgranger", year="2526")

    res = client.get("me/2526/personal-tasks", auth=HPOTTER_CREDENTIALS)

    assert res.status_code == HTTP_200_OK
    tasks = res.json()

    assert len(tasks) == 1, f"Expected 1 task, got {len(tasks)}"
    assert all(
        task["username"] == "hpotter" for task in tasks
    ), "Response contains tasks for other users"
    assert all(
        task["year"] == "2526" for task in tasks
    ), "Response contains tasks for other years"


@freeze_time("2026-02-28")
def test_tasks_response_only_contains_incomplete_or_today_tasks(client, task_factory):
    today = "2026-02-28"
    past_date = "2026-02-26"

    task_factory.create(
        username="hpotter", year="2526", task_completed=False, creation_date=past_date
    )
    task_factory.create(
        username="hpotter", year="2526", task_completed=True, creation_date=past_date
    )
    task_factory.create(
        username="hpotter", year="2526", task_completed=True, creation_date=today
    )

    res = client.get("me/2526/personal-tasks", auth=HPOTTER_CREDENTIALS)

    assert res.status_code == HTTP_200_OK
    tasks = res.json()
    assert len(tasks) == 2


def test_create_task_endpoint(client):
    new_task = {
        "title": "Test Task",
        "creation_date": "2026-02-28",
    }
    res = client.post(
        "me/2526/personal-tasks",
        json=new_task,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 201
    created_task = res.json()
    assert created_task["title"] == new_task["title"]
    assert created_task["creation_date"] == new_task["creation_date"]
    assert created_task["username"] == "hpotter"
    assert created_task["year"] == "2526"
    assert created_task["task_completed"] is False

    assert "id" in created_task
    assert created_task["id"] is not None


def test_create_task_with_missing_title_returns_422(client):
    res = client.post(
        "me/2526/personal-tasks",
        json={"creation_date": "2026-02-28"},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == HTTP_422_UNPROCESSABLE_CONTENT


def test_create_task_with_invalid_date_format_returns_422(client):
    res = client.post(
        "me/2526/personal-tasks",
        json={"title": "Test", "creation_date": "28/02/2026"},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == HTTP_422_UNPROCESSABLE_CONTENT


def test_update_task_completion(client, task_factory):
    task = task_factory.create(
        username="hpotter",
        year="2526",
        task_completed=False,
        creation_date="2026-02-28",
    )
    res = client.patch(
        f"me/2526/personal-tasks/{task.id}",
        json={"task_completed": True},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == HTTP_200_OK
    updated_task = res.json()
    assert updated_task["task_completed"] is True


def test_get_task_by_id(client, task_factory):
    task = task_factory.create(
        username="hpotter",
        year="2526",
        task_completed=False,
        creation_date="2026-02-28",
    )
    res = client.get(f"me/2526/personal-tasks/{task.id}", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_200_OK
    retrieved_task = res.json()
    assert retrieved_task["id"] == task.id


def test_get_nonexistent_task_returns_404(client):
    res = client.get("me/2526/personal-tasks/9999", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_404_NOT_FOUND


def test_update_nonexistent_task_returns_404(client):
    res = client.patch(
        "me/2526/personal-tasks/9999",
        json={"task_completed": True},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == HTTP_404_NOT_FOUND


def test_delete_task_endpoint(client, task_factory):
    task = task_factory.create(
        username="hpotter",
        year="2526",
        task_completed=False,
        creation_date="2026-02-28",
    )
    res = client.delete(f"me/2526/personal-tasks/{task.id}", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_204_NO_CONTENT

    get_res = client.get(f"/me/2526/personal-tasks/{task.id}", auth=HPOTTER_CREDENTIALS)
    assert get_res.status_code == HTTP_404_NOT_FOUND


def test_get_task_owned_by_another_user_returns_404(client, task_factory):
    task = task_factory.create(username="hgranger", year="2526")
    res = client.get(f"me/2526/personal-tasks/{task.id}", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_404_NOT_FOUND


def test_update_task_owned_by_another_user_returns_404(client, task_factory):
    task = task_factory.create(username="hgranger", year="2526", task_completed=False)
    res = client.patch(
        f"me/2526/personal-tasks/{task.id}",
        json={"task_completed": True},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == HTTP_404_NOT_FOUND
    assert task.task_completed is False


def test_delete_task_owned_by_another_user_returns_404(client, task_factory):
    task = task_factory.create(username="hgranger", year="2526")
    res = client.delete(f"me/2526/personal-tasks/{task.id}", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_404_NOT_FOUND
