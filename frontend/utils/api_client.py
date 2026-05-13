import os
import requests

BASE_URL = os.getenv(
    "BACKEND_URL",
    "https://drivescout-ai.onrender.com"
)

def search_files(user_query):

    response = requests.get(
        f"{BASE_URL}/ai-search",
        params={"query": user_query},
        timeout=60
    )

    response.raise_for_status()

    return response.json()