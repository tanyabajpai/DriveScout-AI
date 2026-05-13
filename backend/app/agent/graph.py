from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import json

from app.agent.prompts import SYSTEM_PROMPT

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)


def parse_user_query(user_query):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_query)
    ]

    response = llm.invoke(messages)

    return json.loads(response.content)