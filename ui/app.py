'''
### `ui/app.py` — Streamlit Application
Manages `session_id` and `messages` in `st.session_state`.  Renders the conversation
history, a sidebar with service health and session controls, and a chat input box.
On submission, calls `api_client.chat`, displays the response, and annotates it with
the tool names that were called.
'''
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
from ui.api_client import chat


# page config
st.set_page_config(page_title="Atlas AI", layout="centered")

st.title("Atlas AI Assistant")

# initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "default"

# display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input box
user_input = st.chat_input("Ask something:")

if user_input:
    # add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat(user_input, st.session_state.session_id)

            assistant_msg = response.get("response", "No response")
            tools = response.get("tool_calls_made", [])

            st.write(assistant_msg)

            if tools:
                st.caption(f"Tools used: {', '.join(tools)}")

    # store assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_msg
    })