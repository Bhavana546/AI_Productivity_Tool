import streamlit as st
from components.charts import render_chart

st.title("Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Tasks Completed", "42")
col2.metric("Emails Generated", "15")
col3.metric("Meetings Summarized", "8")

st.subheader("Activity Overview")
render_chart()
