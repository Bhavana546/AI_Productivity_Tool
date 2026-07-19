import streamlit as st
from services.email_generator import load_generator

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
