import requests

BASE_URL = "http://127.0.0.1:8000"


def search_files(user_query):
    response = requests.get(
        f"{BASE_URL}/ai-search",
        params={"query": user_query}
    )

    return response.json()