import streamlit as st
from components.sidebar import render_sidebar
from utils.constants import APP_TITLE, APP_ICON

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
render_sidebar()

st.title("⚡ AI Productivity Hub")
st.markdown("""
Welcome to the **AI Productivity Hub**, a Generative AI-powered application designed to help you work smarter!

Use the navigation menu on the left to explore the available tools:
- 📄 **Document Summarizer**: Quickly extract key points from long texts.
- 📧 **Email & Content Generator**: Draft emails or generate ideas efficiently.
- 🤝 **Meeting Notes Summarizer**: Turn your raw meeting notes into concise summaries.
- 📋 **Task Extractor**: Extract actionable tasks and to-dos from your text.
""")
