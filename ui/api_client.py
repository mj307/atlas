'''
### `ui/api_client.py` — `chat`, `health_check`
Synchronous httpx wrappers for the Streamlit UI.  `chat` sends the user message and
session ID to the agent.  `health_check` pings all four `/health` endpoints and returns
a dict of service → "ok"/"unreachable".
'''
import httpx
from shared.config import settings

def chat(message: str, session_id: str = 'default'):
    try:
        response = httpx.post(f"{settings.agent_url}/chat", 
                json={"message":message, "session_id":session_id})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"response": f"Error: {e}"}

    
def health_check():
    pass
