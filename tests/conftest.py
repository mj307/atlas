import pytest
from httpx import AsyncClient, ASGITransport
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from mcp_servers.knowledge_base.main import app as kb_app
from mcp_servers.calculator.main import app as calc_app
from mcp_servers.task_manager.main import app as task_app
from agent.main import app as agent_app


@pytest.fixture
async def kb_client():
    async with AsyncClient(
        transport=ASGITransport(app=kb_app),
        base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
async def calc_client():
    async with AsyncClient(
        transport=ASGITransport(app=calc_app),
        base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
async def task_client():
    async with AsyncClient(
        transport=ASGITransport(app=task_app),
        base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
async def agent_client():
    async with AsyncClient(
        transport=ASGITransport(app=agent_app),
        base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}