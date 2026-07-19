import streamlit as st
from services.summarizer import load_summarizer

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
