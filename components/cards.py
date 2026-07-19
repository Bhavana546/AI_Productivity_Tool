import streamlit as st
def render_card(title, content):
    st.markdown(f"<div style='padding:15px; border-radius:10px; background-color:#1E1E1E; border:1px solid #333; margin-bottom:10px;'><h4>{title}</h4><p>{content}</p></div>", unsafe_allow_html=True)
