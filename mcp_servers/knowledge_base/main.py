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
from mcp_servers.knowledge_base import database

from fastmcp import FastMCP

mcp = FastMCP("Knowledge Base MCP")

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

async def _search_notes(query: str, k: int = 5):
    results = await database.search_notes(query)
    return results[:k]
  
async def _list_notes():
    return await database.list_notes()
  
async def _delete_note(note_id: int):
    return await database.delete_note(note_id)
  
@mcp.tool()
async def store_note(content: str):
    return await _store_note(content)

@mcp.tool()
async def search_notes(query: str, k: int = 5):
    return await _search_notes(query, k)

@mcp.tool()
async def list_notes():
    return await _list_notes()

@mcp.tool()
async def delete_note(note_id: int):
    return await _delete_note(note_id)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    yield
    

app = FastAPI(lifespan=lifespan)

@app.post("/tools/store_note")
async def store(req: StoreNoteRequest, _: str = Depends(verify_mcp_token)):
    res = await _store_note(req.content)
    return {"output": res, "is_error": False}
  
@app.post("/tools/search_notes")
async def search(req: SearchRequest, _: str = Depends(verify_mcp_token)):
    res = await _search_notes(req.query, req.k)
    return {"output": res, "is_error": False}

@app.post("/tools/list_notes")
async def list_all(_: str = Depends(verify_mcp_token)):
    res = await _list_notes()
    return {"output": res, "is_error": False}
  
@app.post("/tools/delete_note")
async def delete(req: DeleteRequest, _: str = Depends(verify_mcp_token)):
    res = await _delete_note(req.note_id)
    return {"output": res, "is_error": False}

  


