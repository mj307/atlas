from fastapi import FastAPI, Depends
from pydantic import BaseModel
from shared.auth import verify_mcp_token
from fastmcp import FastMCP
import ast
import statistics


mcp = FastMCP("Calculator MCP")
app = FastAPI()



class CalcRequest(BaseModel):
    expression: str

class ConvertRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str

class StatRequest(BaseModel):
    numbers: list[float]



def _safe_eval(expr: str):
    allowed_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp,
        ast.Constant, ast.Add, ast.Sub, ast.Mult,
        ast.Div, ast.Pow, ast.Mod, ast.USub
    )

    tree = ast.parse(expr, mode="eval")

    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            raise ValueError("Unsafe expression")

    return eval(compile(tree, "", "eval"))


async def _calculate(expression: str) -> str:
    try:
        result = _safe_eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


async def _convert_units(value: float, from_unit: str, to_unit: str):
    conversions = {
        ("m", "km"): lambda x: x / 1000,
        ("km", "m"): lambda x: x * 1000,
    }
    try:
        return conversions[(from_unit, to_unit)](value)
    except KeyError:
        return f"Error: unsupported conversion {from_unit} → {to_unit}"


async def _compute_stats(numbers: list[float]):
    return {
        "mean": statistics.mean(numbers),
        "median": statistics.median(numbers),
        "min": min(numbers),
        "max": max(numbers),
    }


@mcp.tool()
async def calculate(expression: str):
    return await _calculate(expression)

@mcp.tool()
async def convert_units(value: float, from_unit: str, to_unit: str):
    return await _convert_units(value, from_unit, to_unit)

@mcp.tool()
async def compute_stats(numbers: list[float]):
    return await _compute_stats(numbers)



@app.post("/tools/calculate")
async def calculate_endpoint(
    req: CalcRequest,
    _: str = Depends(verify_mcp_token)
):
    result = await _calculate(req.expression)
    return {"result": result, "success": True}


@app.post("/tools/convert")
async def convert_endpoint(
    req: ConvertRequest,
    _: str = Depends(verify_mcp_token)
):
    result = await _convert_units(req.value, req.from_unit, req.to_unit)
    return {"result": result, "success": True}


@app.post("/tools/compute_stats")
async def stats_endpoint(
    req: StatRequest,
    _: str = Depends(verify_mcp_token)
):
    result = await _compute_stats(req.numbers)
    return {"result": result, "success": True}


@app.get("/health")
async def health():
    return {"status": "ok"}