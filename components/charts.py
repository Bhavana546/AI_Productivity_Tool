import streamlit as st
import plotly.express as px
import pandas as pd

def render_chart():
    st.bar_chart([1,2,3])

def render_productivity_chart():
    data = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Productivity": [65, 80, 75, 90, 85, 40, 50]
    }
    df = pd.DataFrame(data)
    fig = px.line(df, x="Day", y="Productivity", title="Weekly Productivity", markers=True)
    st.plotly_chart(fig, use_container_width=True)
