import streamlit as st
from utils.constants import APP_TITLE, APP_ICON

def render_sidebar():
    st.sidebar.title(f"{APP_ICON} {APP_TITLE}")

    if "user_name" not in st.session_state:
        st.session_state["user_name"] = "User"

    st.sidebar.markdown(f"Welcome back, **{st.session_state['user_name']}**!")
    st.sidebar.markdown("---")

    st.sidebar.page_link("app.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/AI_Command_Center.py", label="AI Command Center", icon="🎛️")
    st.sidebar.page_link("pages/Dashboard.py", label="Dashboard", icon="📊")
    st.sidebar.page_link("pages/AI_Task_Manager.py", label="Task Manager", icon="✅")
    st.sidebar.page_link("pages/Document_Summarizer.py", label="Summarizer", icon="📄")
    st.sidebar.page_link("pages/Email_Generator.py", label="Email Generator", icon="📧")
    st.sidebar.page_link("pages/Meeting_Assistant.py", label="Meeting Notes", icon="🎤")
    st.sidebar.page_link("pages/AI_Chat.py", label="AI Assistant", icon="🤖")
    st.sidebar.page_link("pages/Smart_Planner.py", label="Planner", icon="📅")
    st.sidebar.page_link("pages/Settings.py", label="Settings", icon="⚙️")
