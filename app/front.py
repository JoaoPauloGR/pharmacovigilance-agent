import json, os
import httpx
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

def token_stream(question: str):
    with httpx.stream("POST", f"{API_URL}/v1/chat/stream",
                      json={"message": question}, timeout=120) as r: 
        r.raise_for_status()
        for line in r.iter_lines():
            if not line.startswith("data: "):
                continue
            payload = line.removeprefix("data: ")
            if payload == "[DONE]":
                break
            yield json.loads(payload)["message"]["content"]


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        answer = st.write_stream(token_stream(prompt))
        st.session_state.messages.append({"role": "assistant", "content": answer})