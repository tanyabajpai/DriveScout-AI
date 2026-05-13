import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.agent.drive_search_tool import drive_search_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

llm_with_tools = llm.bind_tools([drive_search_tool])

CHAT_SYSTEM_PROMPT = """
You are DriveScout AI, a helpful assistant that finds files in Google Drive.

When a user asks to find files, use the drive_search_tool with appropriate 
search_term and file_type arguments.

Supported file_type values: pdf, image, video, spreadsheet, document

After getting results, give a friendly summary.
If no files found, tell the user politely.
"""

def run_agent(user_message: str, chat_history: list = None) -> dict:
    if chat_history is None:
        chat_history = []

    messages = [SystemMessage(content=CHAT_SYSTEM_PROMPT)]

    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=user_message))

    response = llm_with_tools.invoke(messages)

    files = []

    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "drive_search_tool":
                files = drive_search_tool.invoke(tool_call["args"])

        if files:
            file_names = "\n".join([f"- {f['name']}" for f in files[:10]])
            summary = f"I found {len(files)} file(s) for you:\n{file_names}"
        else:
            summary = "I couldn't find any matching files in your Google Drive."

        return {"response": summary, "files": files}

    return {"response": response.content, "files": []}