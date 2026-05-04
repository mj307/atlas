import pytest

@pytest.mark.asyncio
async def test_store_and_list(kb_client, auth_headers):
    await kb_client.post(
        "/tools/store_note",
        json={"content": "hello world"},
        headers=auth_headers
    )

    res = await kb_client.post(
        "/tools/list_notes",
        headers=auth_headers
    )

    data = res.json()["result"]
    assert any("hello world" in n["content"] for n in data)


@pytest.mark.asyncio
async def test_search_hit_and_miss(kb_client, auth_headers):
    await kb_client.post(
        "/tools/store_note",
        json={"content": "mcp is cool"},
        headers=auth_headers
    )

    hit = await kb_client.post(
        "/tools/search_notes",
        json={"query": "mcp", "k": 5}
    )
    assert len(hit.json()["result"]) > 0

    miss = await kb_client.post(
        "/tools/search_notes",
        json={"query": "nonexistent", "k": 5}
    )
    assert miss.json()["result"] == []


@pytest.mark.asyncio
async def test_delete(kb_client, auth_headers):
    res = await kb_client.post(
        "/tools/store_note",
        json={"content": "to delete"},
        headers=auth_headers
    )
    note_id = res.json()["result"]["id"]

    await kb_client.post(
        "/tools/delete_note",
        json={"note_id": note_id},
        headers=auth_headers
    )

    res = await kb_client.post(
        "/tools/list_notes",
        headers=auth_headers
    )
    assert all(n["id"] != note_id for n in res.json()["result"])