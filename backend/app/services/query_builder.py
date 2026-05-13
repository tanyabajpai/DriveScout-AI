import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

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

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def parse_query(user_query: str) -> dict:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_query)
    ]
    response = llm.invoke(messages)
    text = response.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())