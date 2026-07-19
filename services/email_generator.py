import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_generator():
    return pipeline("text-generation", model="distilgpt2")
