import streamlit as st
from services.summarizer import load_summarizer
from services.prompt_engine import get_document_summary_prompt
from services.ai_service import get_ai_response
from utils.file_handler import load_file

st.title("📄 Document Summarizer")

# Sidebar for API Key
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

st.markdown("Upload your document (TXT, PDF, DOCX) or paste the text below to summarize it.")

uploaded_file = st.file_uploader("Upload Document", type=['txt', 'pdf', 'docx'])

file_text = ""
if uploaded_file:
    file_text = load_file(uploaded_file)
    if file_text:
        st.success("File uploaded successfully!")

text = st.text_area("Or paste your document text here:", value=file_text, height=300)
if st.button("Summarize"):
    if text:
        with st.spinner("Summarizing..."):
            if api_key:
                try:
                    prompt = get_document_summary_prompt(text)
                    summary_data = get_ai_response(prompt, api_key)
                    st.success("Summary generated successfully!")

                    # Store summary data in session state for later steps
                    st.session_state['summary_data'] = summary_data

                except Exception as e:
                    st.error(f"Error generating summary with Gemini: {str(e)}")
            else:
                summarizer = load_summarizer()
                summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
                st.success("Summary generated!")
                st.session_state['summary_data'] = {"Executive Summary": summary[0]['summary_text']}
                st.session_state['is_local_summary'] = True
    else:
        st.warning("Please enter some text to summarize.")

if 'summary_data' in st.session_state:
    summary_data = st.session_state['summary_data']

    if st.session_state.get('is_local_summary', False):
         st.write(summary_data["Executive Summary"])
         markdown_output = "# Document Summary\n\n"
         markdown_output += f"{summary_data['Executive Summary']}\n\n"
    else:
        if "Executive Summary" in summary_data:
            with st.expander("Executive Summary", expanded=True):
                st.write(summary_data["Executive Summary"])

        if "Key Insights" in summary_data:
            with st.expander("Key Insights", expanded=True):
                for insight in summary_data["Key Insights"]:
                    st.write(f"- {insight}")

        if "Important Dates" in summary_data:
            with st.expander("Important Dates", expanded=True):
                for date in summary_data["Important Dates"]:
                    st.write(f"- {date}")

        if "Action Items" in summary_data:
            with st.expander("Action Items", expanded=True):
                for item in summary_data["Action Items"]:
                    st.write(f"- {item}")

        if "Questions Generated" in summary_data:
            with st.expander("Questions Generated", expanded=True):
                for question in summary_data["Questions Generated"]:
                    st.write(f"- {question}")

        if "Keywords" in summary_data:
            with st.expander("Keywords", expanded=True):
                st.write(", ".join(summary_data["Keywords"]))

        # Generate Markdown for Export/Copy
        markdown_output = "# Document Summary\n\n"
        if "Executive Summary" in summary_data:
            markdown_output += "## Executive Summary\n"
            markdown_output += f"{summary_data['Executive Summary']}\n\n"
        if "Key Insights" in summary_data:
            markdown_output += "## Key Insights\n"
            for insight in summary_data["Key Insights"]:
                markdown_output += f"- {insight}\n"
            markdown_output += "\n"
        if "Important Dates" in summary_data:
            markdown_output += "## Important Dates\n"
            for date in summary_data["Important Dates"]:
                markdown_output += f"- {date}\n"
            markdown_output += "\n"
        if "Action Items" in summary_data:
            markdown_output += "## Action Items\n"
            for item in summary_data["Action Items"]:
                markdown_output += f"- {item}\n"
            markdown_output += "\n"
        if "Questions Generated" in summary_data:
            markdown_output += "## Questions Generated\n"
            for question in summary_data["Questions Generated"]:
                markdown_output += f"- {question}\n"
            markdown_output += "\n"
        if "Keywords" in summary_data:
            markdown_output += "## Keywords\n"
            markdown_output += f"{', '.join(summary_data['Keywords'])}\n\n"

    st.markdown("---")
    st.subheader("Export Options")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ Download Summary (Markdown)",
            data=markdown_output,
            file_name="document_summary.md",
            mime="text/markdown"
        )
    with col2:
        st.markdown("**Copy Summary:** (Hover over block to copy)")
        st.code(markdown_output, language='markdown')
