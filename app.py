import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

@st.cache_resource
def load_generator():
    return pipeline("text-generation", model="distilgpt2")

st.set_page_config(page_title="AI Productivity Hub", page_icon="⚡", layout="wide")

st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose a tool", [
    "Home",
    "Document Summarizer",
    "Email & Content Generator",
    "Meeting Notes Summarizer",
    "Task Extractor"
])

if app_mode == "Home":
    st.title("⚡ AI Productivity Hub")
    st.markdown("""
    Welcome to the **AI Productivity Hub**, a Generative AI-powered application designed to help you work smarter!

    Use the navigation menu on the left to explore the available tools:
    - 📄 **Document Summarizer**: Quickly extract key points from long texts.
    - 📧 **Email & Content Generator**: Draft emails or generate ideas efficiently.
    - 🤝 **Meeting Notes Summarizer**: Turn your raw meeting notes into concise summaries.
    - 📋 **Task Extractor**: Extract actionable tasks and to-dos from your text.
    """)

elif app_mode == "Document Summarizer":
    st.title("📄 Document Summarizer")
    text = st.text_area("Paste your document text here:", height=300)
    if st.button("Summarize"):
        if text:
            with st.spinner("Summarizing..."):
                summarizer = load_summarizer()
                summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
                st.success("Summary generated!")
                st.write(summary[0]['summary_text'])
        else:
            st.warning("Please enter some text to summarize.")

elif app_mode == "Email & Content Generator":
    st.title("📧 Email & Content Generator")
    prompt = st.text_area("What do you want to write about? (e.g., 'Write an email to my team about the upcoming project deadline')", height=150)
    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating..."):
                generator = load_generator()
                output = generator(prompt, max_length=200, num_return_sequences=1)
                st.success("Content generated!")
                st.write(output[0]['generated_text'])
        else:
            st.warning("Please enter a prompt.")

elif app_mode == "Meeting Notes Summarizer":
    st.title("🤝 Meeting Notes Summarizer")
    notes = st.text_area("Paste your raw meeting notes here:", height=300)
    if st.button("Summarize Notes"):
        if notes:
            with st.spinner("Summarizing..."):
                summarizer = load_summarizer()
                summary = summarizer(notes, max_length=150, min_length=40, do_sample=False)
                st.success("Meeting summary generated!")
                st.write(summary[0]['summary_text'])
        else:
            st.warning("Please enter meeting notes.")

elif app_mode == "Task Extractor":
    st.title("📋 Task Extractor")
    task_text = st.text_area("Paste your text to extract tasks from:", height=300)
    if st.button("Extract Tasks"):
        if task_text:
            with st.spinner("Extracting tasks..."):
                generator = load_generator()
                prompt = "Extract tasks and to-dos from the following text:\n" + task_text + "\nTasks:\n- "
                output = generator(prompt, max_length=150, num_return_sequences=1)
                st.success("Tasks extracted!")
                st.write(output[0]['generated_text'])
        else:
            st.warning("Please enter some text to extract tasks from.")
