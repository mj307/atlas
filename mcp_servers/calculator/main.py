from fastapi import FastAPI, Depends
from pydantic import BaseModel
from shared.auth import verify_mcp_token
import ast

app = FastAPI()


class CalcRequest(BaseModel):
    expression: str

class ConvertRequest(BaseModel): # converts between units
    value: float
    from_unit: str
    to_unit: str

class StatRequest(BaseModel): # descriptive
    numbers: list[float]


'''
### `mcp_servers/calculator/main.py`
- `_safe_eval(expression)` — walks the AST and whitelists only arithmetic/math nodes;
  raises `ValueError` for any unsafe construct (no `import`, no `__builtins__`, etc.)
- `_calculate`, `_convert_units`, `_statistics` — pure async functions (no I/O, still
  async so they compose cleanly with the rest of the async stack)
- Three `POST /tools/*` endpoints
'''

# set up the valid eval operations

async def _calculate(expression: str) -> str:
    try:
        result = eval(expression) # this isn't safe yet # turn safe
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

async def _convert_units(value:float, from_unit:str, to_unit: str):
    conversions = {("m","km"):lambda x:x/1000,
                   ("km","m"): lambda x:x*1000}
    try:
        f = conversions[(from_unit, to_unit)]
        res = f(value)
        return res
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
    
@app.post("/tools/calculate")
async def calculate(
    req: CalcRequest,
    _: str = Depends(verify_mcp_token)
):
    #print("Received:", req.expression)
    result = await _calculate(req.expression)
    #print("Returning:", result)
    return {"result": result, "success": True}

@app.post('/tools/convert')
async def convert_units(req:ConvertRequest, _:str = Depends(verify_mcp_token)):
    res = await _convert_units(req.value, req.from_unit, req.to_unit)
    return {"result": res, "success": True}


@app.post("/tools/compute_stats")
async def compute_stats(req: StatRequest, _:str = Depends(verify_mcp_token)):
    res = await _compute_stats(req.numbers)
    return {"result": res, "success": True}


# check to make sure app is running ok
@app.get("/health")
async def health():
    return {"status": "ok"}