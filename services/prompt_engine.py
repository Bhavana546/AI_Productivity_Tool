def get_task_extraction_prompt(user_input: str) -> str:
    """
    Generates a prompt to extract tasks from natural language input into structured JSON.
    """
    return f"""You are a professional AI task manager. Your goal is to extract tasks from the user's natural language input and convert them into a structured JSON array.

Analyze the following input:
"{user_input}"

Extract each task and provide the following details for each:
- Task Title: A short, clear title.
- Description: A brief description of what needs to be done.
- Priority: Set as "High", "Medium", or "Low" based on urgency or context.
- Deadline: The mentioned deadline, or "None" if not specified.
- Estimated Duration: The estimated time to complete, or "Not specified".
- Category: A logical category (e.g., "Work", "Personal", "Study").
- Status: Set to "Pending" by default.
- Suggested Order: An integer indicating the suggested order of execution (1 being the first).

CRITICAL INSTRUCTIONS:
- You must return ONLY a valid JSON array of objects.
- DO NOT wrap the output in markdown blocks (e.g., ```json ... ```).
- DO NOT return any text outside of the JSON array.
- The output must be parseable by Python's `json.loads()` directly.

Format the output strictly as a JSON array like this:
[
  {{
    "Task Title": "Example Title",
    "Description": "Example description",
    "Priority": "High",
    "Deadline": "Tomorrow",
    "Estimated Duration": "2 hours",
    "Category": "Work",
    "Status": "Pending",
    "Suggested Order": 1
  }}
]
"""
