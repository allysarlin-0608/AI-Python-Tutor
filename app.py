import streamlit as st

st.title("AI Python Tutor")

st.write("Learn Python through conversation with your AI tutor.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask a Python question...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        st.write("Your AI response will appear here.")

    st.session_state.messages.append({
        "role": "assistant",
        "content": "Your AI response will appear here."
    })
