'''
### `mcp_servers/task_manager/database.py`
Schema: `id`, `title`, `description`, `priority` (low/medium/high), `status`
(pending/completed), `created_at`.
Functions: `init_db`, `insert_task`, `list_tasks`, `complete_task`, `delete_task`.
'''

import aiosqlite
DB_PATH = "tasks.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS tasks (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             title TEXT,
                             description TEXT,
                             priority TEXT CHECK(priority IN ('low', 'medium', 'high')),
                             status TEXT CHECK(status IN ('pending','completed')),
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP                            
                         ) 
                         """)
        await db.commit()
    
# insert task
async def insert_task(title: str, description: str, priority: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO tasks (title, description, priority, status)
            VALUES (?,?,?, 'pending')
            """, (title, description, priority)
        )
        await db.commit()

async def list_tasks():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id, title, description, priority, status FROM tasks") 
        rows = await cursor.fetchall()
        
        return [{
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "priority": r[3],
            "status": r[4]
        } for r in rows]

async def complete_task(task_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE tasks SET status = 'completed' WHERE id=?", (task_id,)
        )
        await db.commit()
        return {"completed": task_id}
    
async def delete_task(task_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        )
        await db.commit()
        return {"deleted": task_id}

        
        
        