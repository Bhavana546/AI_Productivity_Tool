import json
import google.generativeai as genai
from services.prompt_engine import get_planner_prompt

def generate_schedule(tasks: str, available_hours: float, start_time: str, break_duration: int, max_focus_length: int, api_key: str) -> dict:
    """
    Calls the Gemini API to generate an optimized daily schedule from tasks and preferences.
    """
    if not api_key:
        raise ValueError("API key is required.")

    genai.configure(api_key=api_key)

    # Using gemini-1.5-flash as the default model
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = get_planner_prompt(
        tasks=tasks,
        available_hours=available_hours,
        start_time=start_time,
        break_duration=break_duration,
        max_focus_length=max_focus_length
    )

    response = model.generate_content(prompt)

    response_text = response.text.strip()

    # Handle potential markdown wrapping just in case the model ignores instructions
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    elif response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    try:
        schedule_data = json.loads(response_text)
        if not isinstance(schedule_data, dict) or 'schedule' not in schedule_data or 'tips' not in schedule_data:
             raise ValueError("Expected a JSON object with 'schedule' and 'tips' keys.")
        return schedule_data
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {response_text}")
        raise ValueError("The model did not return a valid JSON format.") from e
