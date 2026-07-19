import streamlit as st
from services.email_generator import load_generator

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
