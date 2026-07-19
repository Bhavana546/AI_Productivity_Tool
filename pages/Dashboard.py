import streamlit as st
from components.sidebar import render_sidebar
from components.charts import render_productivity_chart
from utils.constants import APP_TITLE, APP_ICON

st.set_page_config(page_title=f"Dashboard | {APP_TITLE}", page_icon=APP_ICON, layout="wide")
render_sidebar()

# Welcome Section
st.markdown("## Good Morning,")
st.markdown("### Welcome back to AI Productivity Hub")
st.markdown("---")

# Statistics Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Tasks", "12")
with col2:
    st.metric("Completed Tasks", "8")
with col3:
    st.metric("Pending Tasks", "4")
with col4:
    st.metric("Productivity Score", "85%")

st.markdown("---")

# Main Content Layout
main_col1, main_col2 = st.columns([2, 1])

with main_col1:
    # Productivity Chart
    st.subheader("Productivity Chart")
    render_productivity_chart()

    # Recent Activity
    st.subheader("Recent Activity")
    st.markdown("""
    * 📄 Summarized 'Q3 Marketing Report'
    * 📧 Generated email to 'Client X'
    * ✅ Completed task 'Update website copy'
    * 🎤 Extracted notes from 'Weekly Sync'
    """)

with main_col2:
    # Today's Schedule
    st.subheader("Today's Schedule")
    st.markdown("""
    **09:00 AM** - Team Standup

    **11:00 AM** - Client Meeting

    **02:00 PM** - Project Review

    **04:30 PM** - Inbox Zero
    """)

    st.markdown("---")

    # Quick Actions
    st.subheader("Quick Actions")
    if st.button("➕ Add Task", use_container_width=True):
        st.switch_page("pages/AI_Task_Manager.py")
    if st.button("📄 Summarize Document", use_container_width=True):
        st.switch_page("pages/Document_Summarizer.py")
    if st.button("📧 Generate Email", use_container_width=True):
        st.switch_page("pages/Email_Generator.py")
    if st.button("🎤 Meeting Notes", use_container_width=True):
        st.switch_page("pages/Meeting_Assistant.py")
    if st.button("🤖 AI Assistant", use_container_width=True):
        st.switch_page("pages/AI_Chat.py")
