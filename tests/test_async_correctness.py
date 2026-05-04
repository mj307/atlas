import pytest
import asyncio
import time


async def slow():
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_async_faster_than_sequential():
    start = time.time()
    for _ in range(5):
        await slow()
    sequential = time.time() - start

    start = time.time()
    await asyncio.gather(*(slow() for _ in range(5)))
    concurrent = time.time() - start

    assert concurrent < sequential


def test_all_tools_are_async():
    from mcp_servers.knowledge_base.main import store_note
    assert asyncio.iscoroutinefunction(store_note)