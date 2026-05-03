from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).resolve().parents[1]))
from agent.graph import agent_graph

app = FastAPI()

'''
### `agent/main.py` — FastAPI Agent Service
Single `POST /chat` endpoint.  Receives `ChatRequest(message, session_id)`, invokes
`agent_graph.ainvoke(state)`, collects tool call names from intermediate messages,
returns `ChatResponse(response, session_id, tool_calls_made)`.
'''

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    tool_calls_made: list[str]

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # agent runs
    result = await agent_graph.ainvoke({
        "messages": [HumanMessage(content=req.message)]
    })
    # entire conversation is stored in messages
    '''
    messages looks like:
    HumanMessage (what the human wrote to the ai)
    AIMessage
    ToolMessage
    AIMessage 
    '''
    messages = result["messages"]
    tool_calls = []
    for msg in messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for call in msg.tool_calls:
                tool_calls.append(call["name"]) # this extracts the tool name

    final_msg = messages[-1].content

    return ChatResponse(
        response=final_msg,
        session_id=req.session_id,
        tool_calls_made=tool_calls
    )
    
        


