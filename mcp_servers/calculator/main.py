from fastapi import FastAPI, Depends
from pydantic import BaseModel
from shared.auth import verify_mcp_token
app = FastAPI()


class CalcRequest(BaseModel):
    expression: str


async def _calculate(expression: str) -> str:
    try:
        result = eval(expression)  # temp code, just for testing
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# define the api endpoint
@app.post("/tools/calculate")
async def calculate(
    req: CalcRequest,
    _: str = Depends(verify_mcp_token)
):
    print("Received:", req.expression)
    result = await _calculate(req.expression)
    print("Returning:", result)
    return {"result": result, "success": True}


# check to make sure app is running ok
@app.get("/health")
async def health():
    return {"status": "ok"}