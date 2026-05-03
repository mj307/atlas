'''
**Task Manager MCP** (port 8003)
Tracks a TODO list in a local SQLite database.
Tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`.
'''
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager

from shared.auth import verify_mcp_token
from fastmcp import FastMCP

from mcp_servers.task_manager import database

mcp = FastMCP("Task Manager MCP")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    yield

app = FastAPI(lifespan=lifespan)

class CreateTaskRequest(BaseModel):
    title: str
    description: str
    priority: str  


class TaskIdRequest(BaseModel):
    task_id: int


async def _create_task(title: str, description: str, priority: str):
    task_id = await database.insert_task(title, description, priority)
    return {"id": task_id}


async def _list_tasks():
    return await database.list_tasks()


async def _complete_task(task_id: int):
    return await database.complete_task(task_id)


async def _delete_task(task_id: int):
    return await database.delete_task(task_id)


@mcp.tool()
async def create_task(title: str, description: str, priority: str):
    """Create a new task."""
    return await _create_task(title, description, priority)


@mcp.tool()
async def list_tasks():
    """List all tasks."""
    return await _list_tasks()


@mcp.tool()
async def complete_task(task_id: int):
    """Mark a task as completed."""
    return await _complete_task(task_id)


@mcp.tool()
async def delete_task(task_id: int):
    """Delete a task."""
    return await _delete_task(task_id)



@app.post("/tools/create_task")
async def create_task_endpoint(
    req: CreateTaskRequest,
    _: str = Depends(verify_mcp_token)
):
    result = await _create_task(req.title, req.description, req.priority)
    return {"result": result, "success": True}


@app.post("/tools/list_tasks")
async def list_tasks_endpoint(
    _: str = Depends(verify_mcp_token)
):
    result = await _list_tasks()
    return {"result": result, "success": True}


@app.post("/tools/complete_task")
async def complete_task_endpoint(
    req: TaskIdRequest,
    _: str = Depends(verify_mcp_token)
):
    result = await _complete_task(req.task_id)
    return {"result": result, "success": True}


@app.post("/tools/delete_task")
async def delete_task_endpoint(
    req: TaskIdRequest,
    _: str = Depends(verify_mcp_token)
):
    result = await _delete_task(req.task_id)
    return {"result": result, "success": True}


@app.get("/")
async def root():
    return {"message": "Task Manager MCP running"}


@app.get("/health")
async def health():
    return {"status": "ok"}