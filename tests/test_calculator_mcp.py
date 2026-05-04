import pytest

@pytest.mark.asyncio
async def test_basic_math(calc_client):
    res = await calc_client.post(
        "/tools/calculate",
        json={"expression": "2 + 2"}
    )
    assert res.json()["result"] == 4


@pytest.mark.asyncio
async def test_sqrt(calc_client):
    res = await calc_client.post(
        "/tools/calculate",
        json={"expression": "sqrt(16)"}
    )
    assert res.json()["result"] == 4


@pytest.mark.asyncio
async def test_safe_eval_blocks_code(calc_client):
    res = await calc_client.post(
        "/tools/calculate",
        json={"expression": "__import__('os').system('rm -rf /')"}
    )
    assert res.status_code != 200