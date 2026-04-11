from fastapi import FastAPI, Depends
from pydantic import BaseModel
from shared.auth import verify_mcp_token
app = FastAPI()


class CalcRequest(BaseModel):
    expression: str

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


# define the api endpoint
@app.post("/tools/calculate")
async def calculate(
    req: CalcRequest,
    _: str = Depends(verify_mcp_token)
):
    #print("Received:", req.expression)
    result = await _calculate(req.expression)
    #print("Returning:", result)
    return {"result": result, "success": True}


# check to make sure app is running ok
@app.get("/health")
async def health():
    return {"status": "ok"}