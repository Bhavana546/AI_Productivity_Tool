import streamlit as st
import json
from services.router import classify_intent, route_command
from utils.file_handler import load_file

st.title("🎛️ AI Command Center")
st.markdown("Control your entire productivity hub with natural language commands.")

api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

uploaded_file = st.file_uploader("Optional: Attach a document (PDF, TXT, DOCX)", type=["txt", "pdf", "docx"])
file_content = None
if uploaded_file:
    file_content = load_file(uploaded_file)

if prompt := st.chat_input("What do you want to do? (e.g., 'Summarize this PDF', 'Plan my day')"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not api_key:
            error_msg = "Please provide your Google Gemini API Key in the sidebar."
            st.error(error_msg)
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        else:
            with st.spinner("Analyzing intent..."):
                intent = classify_intent(prompt, api_key)

            if intent == "Unknown":
                error_msg = "Sorry, I couldn't understand your intent. Try rephrasing your command."
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            else:
                st.info(f"Intent Recognized: **{intent}**")

                with st.spinner(f"Executing {intent}..."):
                    response = route_command(prompt, intent, api_key, file_content, st.session_state)

                # Check if response is JSON (try parsing it)
                is_json = False
                try:
                    parsed_response = json.loads(response)
                    is_json = True
                except (ValueError, TypeError):
                    pass

                if is_json:
                     # display as structured data/markdown if it's our JSON format
                     formatted_response = f"```json\n{json.dumps(parsed_response, indent=2)}\n```"
                     st.markdown(formatted_response)
                     st.session_state.chat_history.append({"role": "assistant", "content": formatted_response})
                else:
                     st.markdown(response)
                     st.session_state.chat_history.append({"role": "assistant", "content": response})
