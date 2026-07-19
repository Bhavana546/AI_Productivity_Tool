import streamlit as st
import pandas as pd
from services.task_manager import extract_tasks_from_text

st.title("📋 AI Task Manager")
st.markdown("Extract actionable tasks from your notes using Google Gemini API.")

# Sidebar for API Key
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

if "tasks_df" not in st.session_state:
    # Initialize an empty DataFrame with the required columns
    st.session_state.tasks_df = pd.DataFrame(columns=[
        "Task Title", "Description", "Priority", "Deadline",
        "Estimated Duration", "Category", "Status", "Suggested Order"
    ])

task_text = st.text_area("Paste your text to extract tasks from:", height=150,
                         placeholder="e.g. I need to finish my AI assignment tomorrow, prepare a hackathon presentation by Friday...")

if st.button("Extract Tasks"):
    if not api_key:
        st.error("Please provide your Google Gemini API Key in the sidebar.")
    elif not task_text:
        st.warning("Please enter some text to extract tasks from.")
    else:
        with st.spinner("Extracting tasks using Gemini..."):
            try:
                extracted_tasks = extract_tasks_from_text(task_text, api_key)
                if extracted_tasks:
                    st.success(f"Successfully extracted {len(extracted_tasks)} tasks!")

                    new_df = pd.DataFrame(extracted_tasks)
                    # Merge with existing
                    st.session_state.tasks_df = pd.concat([st.session_state.tasks_df, new_df], ignore_index=True)
                else:
                    st.warning("No tasks were found in the text.")
            except Exception as e:
                st.error(f"Error extracting tasks: {str(e)}")

st.markdown("### Manage Tasks")

if not st.session_state.tasks_df.empty:
    # Data Editor
    edited_df = st.data_editor(
        st.session_state.tasks_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Priority": st.column_config.SelectboxColumn(
                "Priority",
                options=["High", "Medium", "Low"],
                required=True
            ),
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=["Pending", "Complete", "In Progress"],
                required=True
            ),
            "Suggested Order": st.column_config.NumberColumn(
                "Suggested Order",
                min_value=1,
                step=1
            )
        },
        key="task_editor"
    )

    if st.button("Save to session state"):
        st.session_state.tasks_df = edited_df
        st.success("Changes saved successfully!")
else:
    st.info("No tasks yet. Enter some text above to extract tasks!")
