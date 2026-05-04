# Atlas

Atlas is a modular AI agent system that uses **MCP (Model Context Protocol)** to connect an LLM to structured tools like a knowledge base, calculator, and task manager.

## What it does

* Lets an AI agent **store, search, and manage data**
* Uses **tool calling (MCP)** instead of hardcoded logic
* Supports both **agent usage (MCP)** and **HTTP APIs (FastAPI)**

---

## How it works

* **MCP servers** expose tools (e.g. `store_note`, `search_notes`)
* The **agent** decides which tools to call using an LLM
* Tools are executed via HTTP and return structured results

---

## Project Structure

```
atlas/
├── requirements.txt
├── .env.example
├── pytest.ini
├── start_services.sh
│
├── shared/
│
├── mcp_servers/
│   ├── knowledge_base/
│   ├── calculator/
│   └── task_manager/
│
├── agent/
│
├── ui/
│
└── tests/
```

---

## Running the project

```bash
# install dependencies
pip install -r requirements.txt

# start all services
bash start_services.sh
```

---

## Example capabilities

* Store and retrieve notes
* Perform calculations safely
* Manage tasks (create, list, delete)
* Chat with an agent that decides which tools to use

---

## Tech stack

* Python (async)
* FastAPI
* FastMCP
* LangGraph / LangChain
* SQLite (`aiosqlite`)
* Streamlit

---

## Why MCP?

MCP allows the agent to:

* dynamically choose tools
* work with structured inputs/outputs
* stay modular as new tools are added

---

## Notes

* Core logic is shared between MCP tools and FastAPI endpoints
* Services are fully async
* Tests cover tools, agent behavior, and concurrency

---
