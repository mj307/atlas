import httpx
import structlog
from shared.config import settings
from langchain_core.tools import tool

log = structlog.get_logger()

# calculate tool
@tool
async def calculate(expression: str):
    """Evaluate a mathematical expression using the MCP calculator service."""
    log.info("calculate - calculate tool called")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.calculator_url}/tools/calculate",
            headers={
                "Authorization": f"Bearer {settings.mcp_secret_key}",
                "Content-Type": "application/json"
            },
            json={"expression": expression}
        )

        response.raise_for_status()
        data = response.json()
        return data.get("result", "No result returned")

# unit conversion tool
@tool
async def convert_units(value:float, from_unit: str, to_unit: str):
    """Convert units using the MCP calculator service (m ↔ km etc)."""
    log.info("convert tool was called")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.calculator_url}/tools/convert",
            headers = {
                "Authorization": f"Bearer {settings.mcp_secret_key}",
                "Content-Type": "application/json"
            },
            json = {
                "value": value,
                "from_unit": from_unit,
                "to_unit": to_unit
            }
        )
    response.raise_for_status()
    return response.json()['result']

# stats tool
@tool
async def compute_stats(numbers: list[float]) -> str:
    """Compute mean, median, min, max using MCP calculator service."""
    log.info("stats_tool_called", numbers=numbers)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.calculator_url}/tools/compute_stats",
            headers={
                "Authorization": f"Bearer {settings.mcp_secret_key}",
                "Content-Type": "application/json",
            },
            json={"numbers": numbers},
        )

    response.raise_for_status()
    return response.json()["result"]

ALL_TOOLS = [calculate, convert_units, compute_stats]