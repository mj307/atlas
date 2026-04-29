'''
### `mcp_servers/knowledge_base/database.py`
Five async functions: `init_db`, `insert_note`, `search_notes`, `list_notes`,
`delete_note`.  Each opens its own `aiosqlite` connection (safe for async — aiosqlite
serialises writes internally).  `set_db_path(path)` allows tests to redirect to a
temp file.

'''

import asyncio
import aiosqlite

DB_PATH = "knowledge.db"

def set_db_path(path: str):
    global DB_PATH
    DB_PATH = path

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def insert_note(content: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO notes (content) VALUES (?)",
            (content,)
        )
        await db.commit()
        return cursor.lastrowid

async def list_notes():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id, content FROM notes")
        rows = await cursor.fetchall()
        return [{"id": r[0], "content": r[1]} for r in rows]
    


async def delete_note(note_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        await db.commit()
        return {"deleted": note_id}


async def search_notes(query: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, content FROM notes WHERE content LIKE ?",
            (f"%{query}%",)
        )
        rows = await cursor.fetchall()
        return [{"id": r[0], "content": r[1]} for r in rows]