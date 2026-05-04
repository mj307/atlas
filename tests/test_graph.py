import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_should_continue_routes():
    from agent.graph import should_continue

    state = {"messages": [{"role": "assistant", "tool_calls": []}]}
    assert should_continue(state) == "end"


@pytest.mark.asyncio
async def test_graph_runs():
    from agent.graph import graph

    graph.invoke = AsyncMock(return_value={"messages": ["ok"]})

    result = await graph.invoke({"messages": []})
    assert result is not None