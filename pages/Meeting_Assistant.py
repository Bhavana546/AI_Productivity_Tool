import streamlit as st
from services.summarizer import load_summarizer
from services.prompt_engine import get_meeting_summary_prompt
from services.ai_service import get_ai_response
from utils.file_handler import load_file

st.title("🤝 Meeting Notes Summarizer")

# Sidebar for API Key
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

st.markdown("Upload your meeting notes (TXT, PDF, DOCX) or paste them below to extract key information.")

uploaded_file = st.file_uploader("Upload Notes", type=['txt', 'pdf', 'docx'])

file_notes = ""
if uploaded_file:
    file_notes = load_file(uploaded_file)
    if file_notes:
        st.success("File uploaded successfully!")

notes = st.text_area("Or paste your raw meeting notes here:", value=file_notes, height=300)

if st.button("Summarize Notes"):
    if notes:
        with st.spinner("Summarizing..."):
            if api_key:
                try:
                    prompt = get_meeting_summary_prompt(notes)
                    summary_data = get_ai_response(prompt, api_key)
                    st.success("Meeting summary generated successfully!")

                    if "Executive Summary" in summary_data:
                        with st.expander("Executive Summary", expanded=True):
                            st.write(summary_data["Executive Summary"])

                    if "Key Decisions" in summary_data:
                        with st.expander("Key Decisions", expanded=True):
                            for decision in summary_data["Key Decisions"]:
                                st.write(f"- {decision}")

                    if "Action Items" in summary_data:
                        with st.expander("Action Items", expanded=True):
                            for item in summary_data["Action Items"]:
                                st.write(f"- {item}")

                    if "Assigned People" in summary_data:
                        with st.expander("Assigned People", expanded=True):
                            for person in summary_data["Assigned People"]:
                                st.write(f"- {person}")

                    if "Deadlines" in summary_data:
                        with st.expander("Deadlines", expanded=True):
                            for deadline in summary_data["Deadlines"]:
                                st.write(f"- {deadline}")

                    if "Risks" in summary_data:
                        with st.expander("Risks", expanded=True):
                            for risk in summary_data["Risks"]:
                                st.write(f"- {risk}")

                    if "Follow-up Tasks" in summary_data:
                        with st.expander("Follow-up Tasks", expanded=True):
                            for task in summary_data["Follow-up Tasks"]:
                                st.write(f"- {task}")

                except Exception as e:
                    st.error(f"Error generating summary with Gemini: {str(e)}")
            else:
                summarizer = load_summarizer()
                summary = summarizer(notes, max_length=150, min_length=40, do_sample=False)
                st.success("Meeting summary generated!")
                st.write(summary[0]['summary_text'])
    else:
        st.warning("Please enter meeting notes.")
