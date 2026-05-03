'''
**Knowledge Base MCP** (port 8001)
Stores and retrieves free-form notes in a local SQLite database via `aiosqlite`.
Tools: `store_note`, `search_notes`, `list_notes`, `delete_note`.

### `mcp_servers/knowledge_base/main.py`
- `FastMCP("Knowledge Base MCP")` instance with `@mcp.tool()` decorated functions
- `_store_note`, `_search_notes`, `_list_notes`, `_delete_note` — private async
  implementations called by both FastMCP tools and FastAPI endpoints
- `app = FastAPI(lifespan=...)` — lifespan calls `database.init_db()` on startup
- HTTP middleware binds `request_id` and `service` to structlog context vars
- Four `POST /tools/*` endpoints, each requires `Depends(verify_mcp_token)`
'''

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager

from shared.auth import verify_mcp_token
from fastmcp import FastMCP

from mcp_servers.knowledge_base import database

mcp = FastMCP("Knowledge Base MCP")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    yield


app = FastAPI(lifespan=lifespan)


class StoreNoteRequest(BaseModel):
    content: str

class SearchRequest(BaseModel):
    query: str
    k: int = 5

class DeleteRequest(BaseModel):
    note_id: int


async def _store_note(content: str):
    note_id = await database.insert_note(content)
    return {"id": note_id}


async def _search_notes(query: str, k: int):
    return await database.search_notes(query, k)

async def _list_notes():
    return await database.list_notes()

async def _delete_note(note_id: int):
    return await database.delete_note(note_id)


@mcp.tool()
async def store_note(content: str):
    """Store a note in the knowledge base."""
    return await _store_note(content)


@mcp.tool()
async def search_notes(query: str, k: int = 5):
    """Search notes by keyword."""
    return await _search_notes(query, k)


@mcp.tool()
async def list_notes():
    """List all notes."""
    return await _list_notes()


@mcp.tool()
async def delete_note(note_id: int):
    """Delete a note by ID."""
    return await _delete_note(note_id)



@app.post("/tools/store_note")
async def store_note_endpoint(
    req: StoreNoteRequest,
    _: str = Depends(verify_mcp_token)
):
    result = await _store_note(req.content)
    return {"result": result, "success": True}


@app.post("/tools/search_notes")
async def search_notes_endpoint(req: SearchRequest):
    try:
        result = await _search_notes(req.query, req.k)
        return {"result": result, "success": True}
    except Exception as e:
        log.exception("search_notes failed")
        return {"result": [], "success": False, "error": str(e)}


@app.post("/tools/list_notes")
async def list_notes_endpoint(
    _: str = Depends(verify_mcp_token)
):
    result = await _list_notes()
    return {"result": result, "success": True}


@app.post("/tools/delete_note")
async def delete_note_endpoint(
    req: DeleteRequest,
    _: str = Depends(verify_mcp_token)
):
    result = await _delete_note(req.note_id)
    return {"result": result, "success": True}



@app.get("/")
async def root():
    return {"message": "Knowledge Base MCP running"}


@app.get("/health")
async def health():
    return {"status": "ok"}