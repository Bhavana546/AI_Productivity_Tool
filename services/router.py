import json
import pandas as pd
from services.ai_service import get_ai_response
from services.prompt_engine import (
    get_intent_classification_prompt,
    get_document_summary_prompt,
    get_meeting_summary_prompt
)
from services.task_manager import extract_tasks_from_text
from services.planner import generate_schedule
from services.productivity_coach import generate_productivity_insights
from services.email_generator import load_generator

def classify_intent(command: str, api_key: str) -> str:
    """Classify user intent using Gemini."""
    prompt = get_intent_classification_prompt(command)
    try:
        data = get_ai_response(prompt, api_key)
        return data.get("intent", "Unknown")
    except Exception as e:
        print(f"Error classifying intent: {e}")
        return "Unknown"

def route_command(command: str, intent: str, api_key: str, file_content: str = None, session_state=None) -> str:
    """Route the command to the respective service."""
    if intent == "Task Manager":
        text_to_process = f"{command}\n\n{file_content}" if file_content else command
        try:
            tasks = extract_tasks_from_text(text_to_process, api_key)
            if session_state is not None:
                 if 'tasks_df' not in session_state:
                     session_state.tasks_df = pd.DataFrame(tasks)
                 else:
                     session_state.tasks_df = pd.concat([session_state.tasks_df, pd.DataFrame(tasks)], ignore_index=True)
            return json.dumps(tasks, indent=2)
        except Exception as e:
            return f"Error extracting tasks: {e}"

    elif intent == "Smart Planner":
        if session_state is None or 'tasks_df' not in session_state or session_state.tasks_df.empty:
            return "Please add tasks using the Task Manager first before planning."
        try:
            tasks_json = session_state.tasks_df.to_json(orient='records')
            # Default preferences for now if none provided in command
            schedule = generate_schedule(tasks_json, 8.0, "09:00", 15, 90, api_key)
            if session_state is not None:
                session_state.schedule_data = schedule
            return json.dumps(schedule, indent=2)
        except Exception as e:
            return f"Error generating schedule: {e}"

    elif intent == "Email Generator":
        try:
            generator = load_generator()
            output = generator(command, max_length=200, num_return_sequences=1)
            return output[0]['generated_text']
        except Exception as e:
            return f"Error generating email: {e}"

    elif intent == "Document Summarizer":
        text_to_summarize = file_content if file_content else command
        if not text_to_summarize.strip():
             return "Please provide a document to summarize."
        try:
            prompt = get_document_summary_prompt(text_to_summarize)
            summary = get_ai_response(prompt, api_key)
            return json.dumps(summary, indent=2)
        except Exception as e:
            return f"Error summarizing document: {e}"

    elif intent == "Meeting Assistant":
        text_to_summarize = file_content if file_content else command
        if not text_to_summarize.strip():
             return "Please provide meeting notes to summarize."
        try:
            prompt = get_meeting_summary_prompt(text_to_summarize)
            summary = get_ai_response(prompt, api_key)
            return json.dumps(summary, indent=2)
        except Exception as e:
            return f"Error summarizing meeting: {e}"

    elif intent == "Productivity Coach":
        if session_state is None or 'tasks_df' not in session_state or session_state.tasks_df.empty:
            return "Please add tasks using the Task Manager first before getting coaching."
        schedule_data = session_state.get('schedule_data', {})
        try:
            insights = generate_productivity_insights(api_key, session_state.tasks_df, schedule_data)
            return json.dumps(insights, indent=2)
        except Exception as e:
             return f"Error getting coaching: {e}"
    else:
         return "I'm not sure how to handle that intent."
