import json
import google.generativeai as genai
from services.prompt_engine import get_task_extraction_prompt

def extract_tasks_from_text(text: str, api_key: str) -> list:
    """
    Calls the Gemini API to extract tasks from text and returns a list of dictionaries.
    """
    if not api_key:
        raise ValueError("API key is required.")

    genai.configure(api_key=api_key)

    # Using gemini-1.5-flash as the default model
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = get_task_extraction_prompt(text)

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
        tasks = json.loads(response_text)
        if not isinstance(tasks, list):
            raise ValueError("Expected a JSON array.")
        return tasks
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {response_text}")
        raise ValueError("The model did not return a valid JSON format.") from e
