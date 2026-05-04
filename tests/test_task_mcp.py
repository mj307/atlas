import pytest

@pytest.mark.asyncio
async def test_add_and_list(task_client):
    await task_client.post(
        "/tools/add_task",
        json={"title": "test"}
    )

    res = await task_client.post("/tools/list_tasks")
    assert len(res.json()["result"]) > 0


@pytest.mark.asyncio
async def test_complete_and_delete(task_client):
    res = await task_client.post(
        "/tools/add_task",
        json={"title": "to complete"}
    )
    task_id = res.json()["result"]["id"]

    await task_client.post(
        "/tools/complete_task",
        json={"task_id": task_id}
    )

    await task_client.post(
        "/tools/delete_task",
        json={"task_id": task_id}
    )

    res = await task_client.post("/tools/list_tasks")
    assert all(t["id"] != task_id for t in res.json()["result"])