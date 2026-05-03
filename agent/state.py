from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

'''
`TypedDict` with two fields:
- `messages: Annotated[list[BaseMessage], add_messages]` — LangGraph's `add_messages`
  reducer appends new messages rather than replacing the list
- `session_id: str` — passed through for logging; future multi-user sessions would
  use this to load/save conversation history
'''

# not a real class bc it doesnt have any init or methods
# more like a dataclass
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
# add messages merges multiple messages together
# so Annotated + add_messages means that we append messages automatically instead of replacing messages each time

# BaseMessage tells python that the list will have elements of type AIMessage or HumanMessage, etc
