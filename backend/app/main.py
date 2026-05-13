from fastapi import FastAPI
from app.services.drive_service import list_files
from app.services.query_builder import parse_query

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

    try:
        parsed_query = parse_query(query)

        files = list_files(
            search_term=parsed_query.get("search"),
            file_type=parsed_query.get("file_type")
        )

        return {
            "parsed_query": parsed_query,
            "results": files
        }

    except Exception as e:
        return {"error": str(e)}