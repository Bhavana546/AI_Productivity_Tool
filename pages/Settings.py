import streamlit as st

st.title("⚙️ Settings")
st.write("Configure your AI Productivity Hub preferences.")
dark_mode = st.toggle("Enable Dark Mode", value=True)
st.selectbox("Default Summarization Model", ["distilbart-cnn-12-6", "t5-small"])
st.selectbox("Default Text Generation Model", ["distilgpt2", "gpt2"])
if st.button("Save Changes"):
    st.success("Settings saved successfully!")
