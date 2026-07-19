import streamlit as st
import json
import pandas as pd
from services.planner import generate_schedule

st.title("🧠 AI Smart Planner")
st.markdown("Plan your day ahead with an AI-assisted optimized schedule based on your tasks.")

# Sidebar for API Key
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

# Check for tasks in session state
if "tasks_df" not in st.session_state or st.session_state.tasks_df.empty:
    st.warning("No tasks found! Please go to the 'AI Task Manager' to add or extract some tasks first.")
    st.stop()

st.markdown("### Your Preferences")
col1, col2 = st.columns(2)

with col1:
    available_hours = st.number_input("Available working hours today", min_value=1.0, max_value=24.0, value=8.0, step=0.5)
    start_time = st.time_input("Preferred start time", value=pd.to_datetime("09:00").time())

with col2:
    break_duration = st.number_input("Break duration (minutes)", min_value=5, max_value=60, value=15, step=5)
    max_focus_length = st.number_input("Max focus session length (minutes)", min_value=30, max_value=120, value=90, step=15)

if st.button("Generate Schedule"):
    if not api_key:
        st.error("Please provide your Google Gemini API Key in the sidebar.")
    else:
        with st.spinner("Generating your optimized daily schedule..."):
            try:
                # Convert task dataframe to JSON string for the prompt
                tasks_json = st.session_state.tasks_df.to_json(orient='records')

                # Format start time to HH:MM string
                start_time_str = start_time.strftime("%H:%M")

                schedule_data = generate_schedule(
                    tasks=tasks_json,
                    available_hours=available_hours,
                    start_time=start_time_str,
                    break_duration=break_duration,
                    max_focus_length=max_focus_length,
                    api_key=api_key
                )

                # Store the generated schedule in session state to display it even if the page refreshes
                st.session_state.schedule_data = schedule_data
                st.success("Schedule generated successfully!")
            except Exception as e:
                st.error(f"Error generating schedule: {str(e)}")

# Display the schedule if it exists in session state
if "schedule_data" in st.session_state:
    st.markdown("---")
    st.markdown("### 🗓️ Your Daily Schedule")

    schedule_data = st.session_state.schedule_data

    if schedule_data.get("schedule"):
        for item in schedule_data["schedule"]:
            start = item.get("start", "N/A")
            end = item.get("end", "N/A")
            task = item.get("task", "Unknown Task")
            priority = item.get("priority", "N/A")

            with st.container():
                st.markdown(f"""
                <div style="padding: 10px; border-radius: 5px; background-color: rgba(255, 255, 255, 0.05); margin-bottom: 10px; border-left: 5px solid {'#ff4b4b' if priority == 'High' else '#ffa500' if priority == 'Medium' else '#00cc66'};">
                    <strong>{start} - {end}</strong><br>
                    <span style="font-size: 1.1em;">{task}</span> <em>({priority} Priority)</em>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No items scheduled.")

    if schedule_data.get("tips"):
        st.markdown("### 💡 Daily Productivity Tips")
        for tip in schedule_data["tips"]:
            st.markdown(f"- {tip}")

    if st.button("Regenerate Schedule"):
        del st.session_state.schedule_data
        st.rerun()

