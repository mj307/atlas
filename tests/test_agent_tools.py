import pytest
from unittest.mock import patch

@pytest.mark.asyncio
@patch("agent.tools.httpx.AsyncClient.post")
async def test_tool_sends_correct_payload(mock_post):
    mock_post.return_value.json.return_value = {"result": "ok"}

    from agent.tools import store_note_tool

    await store_note_tool.run("hello")

    args, kwargs = mock_post.call_args

    assert "/tools/store_note" in args[0]
    assert kwargs["json"]["content"] == "hello"
    assert "Authorization" in kwargs["headers"]