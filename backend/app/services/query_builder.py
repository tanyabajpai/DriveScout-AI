import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are a Google Drive search assistant.
Convert user requests into structured JSON.
Return ONLY valid JSON, no explanation, no markdown.

Supported file types: pdf, image, video, spreadsheet, document

Rules:
- Use singular words for search terms.
- If user says "reports", return "Report".
- Keep search terms short and clean.
- Use null if no search term or file type is mentioned.

Examples:
User: find pdf reports
Response: {"search_term": "Report", "file_type": "pdf"}

User: show all images
Response: {"search_term": null, "file_type": "image"}

User: find everything
Response: {"search_term": null, "file_type": null}
"""

def parse_query(user_query: str) -> dict:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set in environment")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://drivescout-ai.onrender.com",
            "X-Title": "DriveScout AI"
        },
        json={
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ]
        },
        timeout=30
    )

    data = response.json()

    # Raise full error if something went wrong
    if "choices" not in data:
        raise ValueError(f"OpenRouter error: {data}")

    text = data["choices"][0]["message"]["content"].strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())