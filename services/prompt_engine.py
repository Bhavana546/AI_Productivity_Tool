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

def get_planner_prompt(tasks: str, available_hours: float, start_time: str, break_duration: int, max_focus_length: int) -> str:
    """
    Generates a prompt to create an optimized daily schedule from a list of tasks.
    """
    return f"""You are an expert AI productivity planner. I will provide you with my current tasks and some preferences for my day. Your goal is to create an optimized daily schedule.

Here are my tasks (as a JSON string):
{tasks}

Here are my preferences for today:
- Available working hours: {available_hours} hours
- Preferred start time: {start_time}
- Break duration: {break_duration} minutes per break
- Maximum focus session length: {max_focus_length} minutes

To create the schedule, please adhere to these rules:
- Prioritize urgent and high priority tasks first.
- Balance the workload so it's realistic. Estimate completion times if none are provided, and do not overschedule.
- Schedule breaks between focus sessions (respecting the max focus session length and break duration).
- Minimize context switching where possible.
- Calculate the correct start and end times for each scheduled item, starting from the preferred start time. Use 24-hour HH:MM format.

CRITICAL INSTRUCTIONS:
- You must return ONLY valid JSON.
- DO NOT wrap the output in markdown blocks (e.g., ```json ... ```).
- DO NOT return any text outside of the JSON object.
- The output must be parseable by Python's `json.loads()` directly.

Format the output strictly as a JSON object with this exact structure:
{{
  "schedule": [
    {{
      "start": "09:00",
      "end": "10:30",
      "task": "Complete AI Assignment",
      "priority": "High"
    }}
  ],
  "tips": [
    "Take a 15 minute break after every 90 minutes."
  ]
}}
"""
