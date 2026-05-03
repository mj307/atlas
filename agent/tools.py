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

# knowledge base tools

@tool
async def store_note(content: str):
    """Store a note in the knowledge base."""
    log.info("store_note called", content=content)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.knowledge_base_url}/tools/store_note",
            headers={"Authorization": f"Bearer {settings.mcp_secret_key}"},
            json={"content": content},
        )

    response.raise_for_status()
    data = response.json()

    # KEEP STRUCTURE (DO NOT flatten)
    return data["result"]

@tool
async def search_notes(query: str, k: int = 5):
    """Search notes in the knowledge base."""
    log.info("search_notes called", query=query)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.knowledge_base_url}/tools/search_notes",
            headers={"Authorization": f"Bearer {settings.mcp_secret_key}"},
            json={"query": query, "k": k},
        )

    response.raise_for_status()
    data = response.json()

    #return data["result"] 
    return "\n".join(
    f"{r['id']}: {r['content']}"
    for r in data["result"]
)


@tool
async def list_notes():
    """List all stored notes."""
    log.info("list_notes called")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.knowledge_base_url}/tools/list_notes",
            headers={"Authorization": f"Bearer {settings.mcp_secret_key}"},
            json={},
        )

    response.raise_for_status()
    data = response.json()

    return data["result"]

@tool
async def delete_note(note_id: int):
    """Delete a note by ID."""
    log.info("delete_note called", note_id=note_id)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.knowledge_base_url}/tools/delete_note",
            headers={"Authorization": f"Bearer {settings.mcp_secret_key}"},
            json={"note_id": note_id},
        )

    response.raise_for_status()
    data = response.json()

    return data["result"]

@tool
async def create_task(title: str, description: str, priority: str):
    """
    Create a task.

    Use this when the user wants to:
    - create a task
    - add a todo
    - remember something to do

    Extract title, description, and priority (low, medium, high).
    """
    log.info("create_task called", title=title)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.task_manager_url}/tools/create_task",
            headers={
                "Authorization": f"Bearer {settings.mcp_secret_key}",
                "Content-Type": "application/json"
            },
            json={
                "title": title,
                "description": description,
                "priority": priority
            }
        )

    response.raise_for_status()
    data = response.json()
    return f"Task created with ID {data['result']['id']}"


@tool
async def list_tasks():
    """
    Use this when the user asks:
    - what tasks do I have
    - list tasks
    - show my todos
    """
    log.info("list_tasks called")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.task_manager_url}/tools/list_tasks",
            headers={
                "Authorization": f"Bearer {settings.mcp_secret_key}",
                "Content-Type": "application/json"
            },
            json={}
        )

    response.raise_for_status()
    data = response.json()
    tasks = data.get("result", [])

    if not tasks:
        return "No tasks found."

    formatted = []
    for t in tasks:
        task_id = t.get("id", "unknown")
        title = t.get("title", "no title")
        priority = t.get("priority", "unknown")
        status = t.get("status", "pending") 

        formatted.append(f"{task_id}. {title} ({priority}, {status})")

    return "\n".join(formatted)
    
@tool
async def complete_task(task_id: int):
    """
    Use this when the user says:
    - complete task
    - mark task as done
    """
    log.info("complete_task called", task_id=task_id)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.task_manager_url}/tools/complete_task",
            headers={
                "Authorization": f"Bearer {settings.mcp_secret_key}",
                "Content-Type": "application/json"
            },
            json={"task_id": task_id}
        )

    response.raise_for_status()
    return f"Task {task_id} marked as completed."

@tool
async def delete_task(task_id: int):
    """
    Use this when the user says:
    - delete task
    - remove task
    """
    log.info("delete_task called", task_id=task_id)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.task_manager_url}/tools/delete_task",
            headers={
                "Authorization": f"Bearer {settings.mcp_secret_key}",
                "Content-Type": "application/json"
            },
            json={"task_id": task_id}
        )

    response.raise_for_status()
    return f"Task {task_id} deleted."





ALL_TOOLS = [
    calculate,
    convert_units,
    compute_stats,
    store_note,
    search_notes,
    list_notes,
    delete_note,
    create_task,
    list_tasks,
    complete_task,
    delete_task,
]