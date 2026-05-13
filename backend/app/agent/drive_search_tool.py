from langchain.tools import tool
from app.services.drive_service import list_files

@tool
def drive_search_tool(search_term: str = None, file_type: str = None) -> list:
    """
    Search Google Drive files by name or file type.
    
    Args:
        search_term: Keyword to search in file names (e.g. "Report", "Invoice")
        file_type: One of pdf, image, video, spreadsheet, document
    
    Returns:
        List of matching files with id, name, mimeType
    """
    files = list_files(search_term=search_term, file_type=file_type)
    if not files:
        return []
    return files