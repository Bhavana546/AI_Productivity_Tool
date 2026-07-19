import streamlit as st
from services.summarizer import load_summarizer

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
