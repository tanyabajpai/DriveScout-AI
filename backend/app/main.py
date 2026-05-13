from fastapi import FastAPI
from app.services.drive_service import list_files
from app.agent.graph import parse_user_query

app = FastAPI()


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

    parsed_query = parse_user_query(query)

    files = list_files(
        search_term=parsed_query.get("search_term"),
        file_type=parsed_query.get("file_type")
    )

    return {
        "user_query": query,
        "parsed_query": parsed_query,
        "total_files": len(files),
        "files": files
    }