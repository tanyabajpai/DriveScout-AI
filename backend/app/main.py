from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from app.services.drive_service import list_files
from app.services.query_builder import parse_query
from app.agent.graph import run_agent

app = FastAPI(title="DriveScout AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "DriveScout AI Backend Running"}


@app.get("/files")
def get_files(search: str = None, file_type: str = None):
    files = list_files(search, file_type)
    return {
        "total_files": len(files),
        "files": files
    }


@app.get("/ai-search")
def ai_search(query: str):
    try:
        parsed = parse_query(query)
        files = list_files(
            search_term=parsed.get("search_term"),
            file_type=parsed.get("file_type")
        )
        return {
            "parsed_query": parsed,
            "total_files": len(files),
            "files": files
        }
    except Exception as e:
        return {"error": str(e)}


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        result = run_agent(request.message, request.history)
        return result
    except Exception as e:
        return {"error": str(e), "response": f"Error: {str(e)}", "files": []}