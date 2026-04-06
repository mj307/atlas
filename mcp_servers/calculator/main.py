from fastapi import FastAPI
from pydantic import BaseModel

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
async def calculate(req: CalcRequest):
    result = await _calculate(req.expression)
    return {"result": result, "success": True}


# check to make sure app is running ok
@app.get("/health")
async def health():
    return {"status": "ok"}