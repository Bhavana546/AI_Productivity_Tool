import json
import google.generativeai as genai
from services.prompt_engine import get_productivity_coach_prompt
import pandas as pd

def generate_productivity_insights(api_key: str, tasks_df: pd.DataFrame, schedule_data: dict) -> dict:
    """
    Generates productivity insights using the Google Gemini API based on user tasks and schedule.
    """
    if not api_key:
        raise ValueError("Google Gemini API Key is required.")

    genai.configure(api_key=api_key)

    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Prepare data for prompt
    completed_tasks = []
    pending_tasks = []
    overdue_tasks = []
    task_priorities = {}
    estimated_workload = 0

    if not tasks_df.empty:
        # Sort out completed, pending
        if 'Status' in tasks_df.columns:
            completed_tasks = tasks_df[tasks_df['Status'] == 'Complete']['Task Title'].tolist()
            pending_tasks_df = tasks_df[tasks_df['Status'].isin(['Pending', 'In Progress'])]
            pending_tasks = pending_tasks_df['Task Title'].tolist()
        else:
            pending_tasks = tasks_df['Task Title'].tolist()

        # Very basic overdue logic based on Deadline if it exists
        if 'Deadline' in tasks_df.columns:
            # Assuming 'Deadline' is a string or datetime, we'll just extract any that say "Overdue" or are past due
            # For simplicity, we just pass the raw deadlines or any that contain "yesterday" etc.
            pass

        if 'Priority' in tasks_df.columns:
            task_priorities = tasks_df['Priority'].value_counts().to_dict()

        # Try to parse estimated duration if possible
        if 'Estimated Duration' in tasks_df.columns:
            # Simple summarization or pass raw string
            pass

    # Format the data into strings for the prompt
    completed_tasks_str = json.dumps(completed_tasks) if completed_tasks else "None"
    pending_tasks_str = json.dumps(pending_tasks) if pending_tasks else "None"
    overdue_tasks_str = "Unknown"  # Simplify or enhance based on data structure

    priorities_str = json.dumps(task_priorities) if task_priorities else "None"

    # Schedule info
    schedule_str = json.dumps(schedule_data.get('schedule', [])) if schedule_data else "None"

    # Estimated Workload (e.g. number of pending tasks and their priorities)
    estimated_workload_str = f"Total Pending: {len(pending_tasks)}"

    # Generate Prompt
    prompt = get_productivity_coach_prompt(
        completed_tasks=completed_tasks_str,
        overdue_tasks=overdue_tasks_str,
        pending_tasks=pending_tasks_str,
        task_priorities=priorities_str,
        today_schedule=schedule_str,
        estimated_workload=estimated_workload_str
    )

    try:
        # Call the Gemini API
        response = model.generate_content(prompt)

        # Extract and clean JSON response
        response_text = response.text
        # In case the model wrapped it in markdown codeblocks
        cleaned_json = response_text.replace("```json", "").replace("```", "").strip()

        # Parse JSON
        insights_data = json.loads(cleaned_json)
        return insights_data

    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse the JSON response from Gemini. Response was: {response.text}") from e
    except Exception as e:
        raise Exception(f"Failed to generate productivity insights: {str(e)}")
