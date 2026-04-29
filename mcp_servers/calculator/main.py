from fastapi import FastAPI, Depends
from pydantic import BaseModel
from shared.auth import verify_mcp_token
import ast
from fastmcp import FastMCP

mcp = FastMCP("Calculator MCP")
app = FastAPI()


# class CalcRequest(BaseModel):
#     expression: str

# class ConvertRequest(BaseModel): # converts between units
#     value: float
#     from_unit: str
#     to_unit: str

# class StatRequest(BaseModel): # descriptive
#     numbers: list[float]

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
'''
### `mcp_servers/calculator/main.py`
- `_safe_eval(expression)` — walks the AST and whitelists only arithmetic/math nodes;
  raises `ValueError` for any unsafe construct (no `import`, no `__builtins__`, etc.)
- `_calculate`, `_convert_units`, `_statistics` — pure async functions (no I/O, still
  async so they compose cleanly with the rest of the async stack)
- Three `POST /tools/*` endpoints
'''



async def _calculate(expression: str) -> str:
    try:
        result = eval(expression) # this isn't safe yet # turn safe
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

async def _convert_units(value: float, from_unit: str, to_unit: str):
    conversions = {
        ("m", "km"): lambda x: x / 1000,
        ("km", "m"): lambda x: x * 1000,
    }
    try:
        f = conversions[(from_unit, to_unit)]
        return f(value)
    except KeyError as e:
        return f"Error {e}"

import statistics
async def _compute_stats(numbers: list[float]):
    try:
        return {
            "mean": statistics.mean(numbers),
            "median": statistics.median(numbers),
            "min": min(numbers),
            "max":max(numbers)
        }
    except Exception as e:
        return f"Error {e}"

# define the api endpoint
@app.get("/")
async def idx():
    return ("hello")
    
@mcp.tool()
async def calculate(expression: str) -> str:
    """Evaluate a mathematical expression like '2 + 2 * 5'."""
    return await _calculate(expression)


@mcp.tool()
async def convert_units(value: float, from_unit: str, to_unit: str):
    """Convert units"""
    return await _convert_units(value, from_unit, to_unit)


@mcp.tool()
async def compute_stats(numbers: list[float]):
    """Compute mean, median, min, and max of a list of numbers."""
    return await _compute_stats(numbers)

# check to make sure app is running ok
@app.get("/health")
async def health():
    return {"status": "ok"}


import asyncio

async def main():
    tools = await mcp.list_tools()
    print(tools)

asyncio.run(main())