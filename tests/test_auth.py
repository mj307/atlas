import pytest

@pytest.mark.asyncio
async def test_auth_missing_header(kb_client):
    res = await kb_client.post("/tools/list_notes")
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_auth_invalid_token(kb_client):
    res = await kb_client.post(
        "/tools/list_notes",
        headers={"Authorization": "Bearer wrong"}
    )
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_auth_valid(kb_client, auth_headers):
    res = await kb_client.post(
        "/tools/list_notes",
        headers=auth_headers
    )
    assert res.status_code == 200