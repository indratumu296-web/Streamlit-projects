import streamlit as st

st.title("Simple Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Type your message ...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    text = prompt.lower()

    if "python" in text:
        reply = "Python is a popular language for AI and data science."
    elif "streamlit" in text:
        reply = "Streamlit is a Python framework for interactive web apps."
    else:
        reply = f"You said: '{prompt}'. I'm a demo chatbot!"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()