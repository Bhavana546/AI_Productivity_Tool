import json
from google import genai

def get_ai_response(prompt: str, api_key: str) -> dict:
    """
    Calls the Gemini API and parses the JSON response.
    """
    if not api_key:
        raise ValueError("API key is required.")

    client = genai.Client(api_key=api_key)

    # Using gemini-1.5-flash as the default model
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt
    )
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
        data = json.loads(response_text)
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {response_text}")
        raise ValueError("The model did not return a valid JSON format.") from e
