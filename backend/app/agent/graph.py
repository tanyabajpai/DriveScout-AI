from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import os

from app.agent.drive_search_tool import drive_search_tool
from app.services.query_builder import parse_query

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

llm_with_tools = llm.bind_tools([drive_search_tool])

CHAT_SYSTEM_PROMPT = """
You are DriveScout AI, a helpful assistant that helps users find files in Google Drive.

When a user asks to find files, use the drive_search_tool with appropriate search_term and file_type.

Supported file types: pdf, image, video, spreadsheet, document

After getting results, summarize them in a friendly way.
If no files are found, tell the user politely.
"""

def run_agent(user_message: str, chat_history: list = None) -> dict:
    """
    Run the agent with tool calling support.
    Returns dict with ai_response text and files list.
    """
    if chat_history is None:
        chat_history = []

    messages = [SystemMessage(content=CHAT_SYSTEM_PROMPT)]
    
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    
    messages.append(HumanMessage(content=user_message))

    # First LLM call - may trigger tool use
    response = llm_with_tools.invoke(messages)
    
    files = []
    
    # Handle tool calls
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "drive_search_tool":
                args = tool_call["args"]
                files = drive_search_tool.invoke(args)
        
        # Build summary response
        if files:
            file_names = "\n".join([f"- {f['name']}" for f in files[:10]])
            summary = f"I found {len(files)} file(s) for you:\n{file_names}"
        else:
            summary = "I couldn't find any matching files in your Google Drive."
        
        return {"response": summary, "files": files}
    
    return {"response": response.content, "files": []}