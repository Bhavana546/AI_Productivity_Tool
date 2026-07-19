import streamlit as st

st.title("💬 AI Chat")
user_input = st.chat_input("Say something")
if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        st.write(f"You said: {user_input}")
