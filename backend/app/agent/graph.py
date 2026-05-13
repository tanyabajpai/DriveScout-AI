import os
import json
import requests
from dotenv import load_dotenv
from app.services.drive_service import list_files

load_dotenv()

SYSTEM_PROMPT = """
You are DriveScout AI, a helpful assistant that finds files in Google Drive.

When a user asks to find files, respond with a JSON object with these fields:
- "action": "search" or "chat"
- "search_term": keyword to search (or null)
- "file_type": one of pdf, image, video, spreadsheet, document (or null)
- "message": friendly response to show the user

If the user is just chatting (not searching), set action to "chat" and reply normally.

Always return valid JSON only. No explanation, no markdown.

Examples:
User: find pdf files
Response: {"action": "search", "search_term": null, "file_type": "pdf", "message": "Let me find PDF files for you!"}

User: find invoices
Response: {"action": "search", "search_term": "Invoice", "file_type": null, "message": "Searching for invoices now!"}

User: hello
Response: {"action": "chat", "search_term": null, "file_type": null, "message": "Hi! I can help you find files in your Google Drive. Try asking me to find PDFs, images, spreadsheets, or search by name!"}
"""

def run_agent(user_message: str, chat_history: list = None) -> dict:
    if chat_history is None:
        chat_history = []

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"response": "Error: OPENROUTER_API_KEY not set in Render environment variables.", "files": []}

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in chat_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://drivescout-ai.onrender.com",
            "X-Title": "DriveScout AI"
        },
        json={
            "model": "qwen/qwen3-8b:free",
            "messages": messages
        },
        timeout=30
    )

    data = response.json()

    if "choices" not in data:
        return {"response": f"API Error: {data}", "files": []}

    text = data["choices"][0]["message"]["content"].strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()

    try:
        parsed = json.loads(text)
    except Exception:
        return {"response": text, "files": []}

    files = []
    if parsed.get("action") == "search":
        files = list_files(
            search_term=parsed.get("search_term"),
            file_type=parsed.get("file_type")
        )
        if files:
            names = "\n".join([f"- {f['name']}" for f in files[:10]])
            reply = f"{parsed.get('message', '')}\n\nFound {len(files)} file(s):\n{names}"
        else:
            reply = "I searched but couldn't find any matching files in your Google Drive."
    else:
        reply = parsed.get("message", text)

    return {"response": reply, "files": files}