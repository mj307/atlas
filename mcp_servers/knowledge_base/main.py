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
