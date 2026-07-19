import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from services.productivity_coach import generate_productivity_insights

st.title("💡 AI Productivity Coach")
st.markdown("Get personalized insights and recommendations based on your tasks and schedule.")

# Sidebar for API Key
api_key = st.sidebar.text_input("Google Gemini API Key", type="password", key="productivity_coach_api_key")

# Check if tasks exist
if "tasks_df" not in st.session_state or st.session_state.tasks_df.empty:
    st.warning("No tasks found! Please go to the 'AI Task Manager' to add or extract some tasks first.")
    st.stop()

if st.button("Generate Productivity Insights"):
    if not api_key:
        st.error("Please provide your Google Gemini API Key in the sidebar.")
    else:
        with st.spinner("Analyzing your tasks and schedule..."):
            try:
                # Fetch schedule data if it exists
                schedule_data = st.session_state.get("schedule_data", {})

                # Fetch tasks
                tasks_df = st.session_state.tasks_df

                # Generate Insights
                insights = generate_productivity_insights(
                    api_key=api_key,
                    tasks_df=tasks_df,
                    schedule_data=schedule_data
                )

                # Store insights in session state
                st.session_state.productivity_insights = insights
                st.success("Insights generated successfully!")
            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")

# Display insights if they exist in session state
if "productivity_insights" in st.session_state:
    insights = st.session_state.productivity_insights

    st.markdown("---")

    # 1. Productivity Score Circular Gauge
    score = insights.get("productivity_score", 0)

    # Create the plotly gauge chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Productivity Score", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#00cc66" if score >= 75 else "#ffa500" if score >= 50 else "#ff4b4b"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(255, 75, 75, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(255, 165, 0, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(0, 204, 102, 0.2)'}
            ],
        }
    ))

    # Adjust layout
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})

    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🚦 Status Overview")
        # Simple progress bars using Streamlit logic
        total_tasks = len(st.session_state.tasks_df)
        completed_tasks = len(st.session_state.tasks_df[st.session_state.tasks_df['Status'] == 'Complete']) if 'Status' in st.session_state.tasks_df.columns else 0

        st.markdown(f"**Tasks Completed:** {completed_tasks} / {total_tasks}")
        if total_tasks > 0:
            st.progress(completed_tasks / total_tasks)

    with col2:
        st.markdown("### 🔥 Burnout Risk")
        burnout_risk = insights.get("burnout_risk", "Unknown")
        risk_color = "red" if burnout_risk.lower() == "high" else "orange" if burnout_risk.lower() == "medium" else "green"
        st.markdown(f"<h3 style='color: {risk_color};'>{burnout_risk}</h3>", unsafe_allow_html=True)

        st.markdown("### 🎯 Focus Tip")
        st.info(insights.get("focus_tip", "Stay focused!"))

        st.markdown("### ⏳ Time Management")
        st.info(insights.get("time_management", "Manage your time well!"))

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 💪 Strengths")
        for strength in insights.get("strengths", []):
            st.markdown(f"- ✅ {strength}")

    with col4:
        st.markdown("### ⚠️ Weaknesses")
        for weakness in insights.get("weaknesses", []):
            st.markdown(f"- ❌ {weakness}")

    st.markdown("---")

    st.markdown("### 📅 Today's Recommendations")
    for rec in insights.get("today_recommendations", []):
        st.markdown(f"- 📌 {rec}")

    st.markdown("### 🚀 Tomorrow's Suggestions")
    for sug in insights.get("tomorrow", []):
        st.markdown(f"- ➡️ {sug}")

    if st.button("Clear Insights"):
        del st.session_state.productivity_insights
        st.rerun()
