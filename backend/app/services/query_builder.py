from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import json

load_dotenv()

SYSTEM_PROMPT = """
You are a Google Drive search assistant.
Convert user requests into structured JSON.
Return ONLY valid JSON, no explanation.

Supported file types: pdf, image, video, spreadsheet, document

Rules:
- Use singular words for search terms.
- If user says "reports", return "Report".
- Keep search terms short and clean.
- Use null if no search term or file type is mentioned.

Example:
User: find pdf reports
Response:
{
    "search_term": "Report",
    "file_type": "pdf"
}

User: show all images
Response:
{
    "search_term": null,
    "file_type": "image"
}
"""

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

def parse_query(user_query: str) -> dict:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_query)
    ]
    response = llm.invoke(messages)
    text = response.content.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())