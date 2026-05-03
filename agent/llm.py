'''
connect to openrouter here
select the model
at a later stage, attach the tools


### `agent/llm.py` — `get_llm(tools)`
Returns a `ChatOpenAI` instance with:
- `model` from `settings.openrouter_model`
- `openai_api_base` set to `https://openrouter.ai/api/v1`
- `openai_api_key` from `settings.openrouter_api_key`
- Extra headers `HTTP-Referer` and `X-Title` as required by OpenRouter
- If `tools` is provided, calls `.bind_tools(tools)` so the LLM knows the tool schemas
'''

from langchain_openai import ChatOpenAI
from shared.config import settings

def get_llm(tools):
    """You are a tool-using agent.

You MUST use tool outputs as the only source of truth.

If a tool returns information, that information is FINAL and must be used directly.

Never say you do not have access to information if a tool has returned it.

Never claim missing memory if a tool has been used in the conversation.

If a tool returns information, you MUST treat it as fact.
Never say you do not have access to information if a tool result exists in the conversation.

Always answer directly from tool output when available.
    """
    llm = ChatOpenAI(
        model=settings.openrouter_model,
        api_key=settings.openrouter_api_key,
        base_url=settings.openai_api_base,
    )

    if tools:
        llm = llm.bind_tools(tools)

    return llm

