from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

SERVICE_ACCOUNT_FILE = "/etc/secrets/credentials.json"

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    service = build("drive", "v3", credentials=credentials)

    return service


def list_files(search_term=None, file_type=None):
    service = get_drive_service()

    query = f"'{FOLDER_ID}' in parents"

    # filename search
    if search_term and search_term.lower() not in [
        "pdf",
        "image",
        "video",
        "spreadsheet",
        "document"
    ]:
        query += f" and name contains '{search_term}'"

    # file type filtering
    mime_types = {
        "pdf": "application/pdf",
        "image": "image/",
        "video": "video/",
        "spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "document": "application/vnd.google-apps.document"
    }

    if file_type:
        if file_type in ["image", "video"]:
            query += f" and mimeType contains '{mime_types[file_type]}'"
        else:
            query += f" and mimeType='{mime_types[file_type]}'"

    results = service.files().list(
        q=query,
        pageSize=20,
        fields="files(id, name, mimeType)"
    ).execute()

    files = results.get("files", [])

    return files