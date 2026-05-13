# 📁 DriveScout AI

An AI-powered conversational Google Drive search assistant built with FastAPI, Streamlit, LangChain, OpenRouter, and the Google Drive API.

---

## 🚀 Live Demo

- **Frontend (Streamlit):** https://drivescout-ai-cxmpuhrruy824q7oxuqstu.streamlit.app/
- **Backend (Render):** `https://drivescout-ai.onrender.com`
- **API Docs:** `https://drivescout-ai.onrender.com/docs`

---

## 🎯 Overview

DriveScout AI lets users search Google Drive files through a natural language chat interface. Instead of manually browsing folders, users simply type conversational queries like:

- *"Find all PDF reports"*
- *"Show me spreadsheets"*
- *"Do you have any images?"*
- *"Find invoices"*

The AI understands the intent, converts it into a structured Google Drive query, retrieves matching files, and presents them with direct Drive links — all through a chat UI.

---

## ✨ Features

- 💬 Conversational chat interface (multi-turn)
- 🤖 AI-powered natural language query parsing
- 📂 Google Drive API integration via Service Account
- 🔍 Search by file name and file type (PDF, image, spreadsheet, video, document)
- 🔗 Direct Google Drive file links in results
- 📊 File type summary (PDF, image, spreadsheet, video counts)
- ⚡ FastAPI backend with `/chat`, `/files`, and `/ai-search` endpoints
- 🌐 Fully deployed (Render + Streamlit Cloud)

---

## 🏗️ System Architecture

```
User (Streamlit Chat UI)
        ↓  POST /chat
FastAPI Backend (Render)
        ↓
OpenRouter LLM (free tier — auto-selects best available model)
        ↓  Structured JSON (action, search_term, file_type)
Google Drive API (Service Account)
        ↓
Files returned with id, name, mimeType
        ↓
Streamlit displays results with Drive links
```

---

## 🧠 How It Works

1. User types a natural language query in the Streamlit chat UI.
2. Frontend sends the message + conversation history to `POST /chat` on the FastAPI backend.
3. The backend calls OpenRouter's LLM with a structured system prompt, which returns a JSON object specifying `action`, `search_term`, and `file_type`.
4. If `action` is `"search"`, the backend queries Google Drive using the `files.list` method with the `q` parameter (filtering by name, mimeType, and parent folder).
5. Matching files are returned with their Google Drive IDs.
6. The frontend displays AI response text + file cards with clickable Drive links.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Python |
| AI / LLM | OpenRouter (free router — auto model selection) |
| Agent Framework | LangChain (tool calling) |
| Drive Integration | Google Drive API v3 (Service Account) |
| Backend Hosting | Render |
| Frontend Hosting | Streamlit Cloud |

---

## 📂 Project Structure

```
DriveScout-AI/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── graph.py           # LLM agent — parses intent, calls Drive
│   │   │   ├── drive_search_tool.py  # LangChain tool for Drive search
│   │   │   └── prompts.py
│   │   ├── config/
│   │   │   └── credentials.json   # Google Service Account (gitignored)
│   │   ├── routes/
│   │   │   └── chat.py
│   │   ├── schemas/
│   │   │   └── search_schema.py
│   │   ├── services/
│   │   │   ├── drive_service.py   # Google Drive API integration
│   │   │   └── query_builder.py   # LLM query parser
│   │   ├── tools/
│   │   │   └── drive_search_tool.py
│   │   └── main.py                # FastAPI app + endpoints
│   ├── requirements.txt
│   └── .env                       # Gitignored
│
├── frontend/
│   ├── utils/
│   │   └── api_client.py          # Backend API calls
│   ├── app.py                     # Streamlit chat UI
│   └── requirements.txt
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/tanyabajpai/DriveScout-AI
cd DriveScout-AI
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id
```

Place your Google Service Account credentials file at:

```
backend/app/config/credentials.json
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`
API docs at: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup

```bash
cd frontend
pip install -r requirements.txt
```

Create a `.streamlit/secrets.toml` file:

```toml
BACKEND_URL = "http://127.0.0.1:8000"
```

Run the frontend:

```bash
streamlit run app.py
```

Frontend runs at: `http://localhost:8501`

---

## 🔑 Google Drive Setup

1. Create a Google Cloud project and enable the **Google Drive API**.
2. Create a **Service Account** and download the `credentials.json` key file.
3. Copy the [sample Drive folder](https://drive.google.com/drive/folders/1qkx58doSeYrcLjHPDysJyVJ36PsSqqlt) into your own Google Drive.
4. Share that folder with your service account's `client_email` (give Viewer access).
5. Copy the folder ID from the URL and set it as `GOOGLE_DRIVE_FOLDER_ID` in your `.env`.

---

## 🌐 Deployment

### Backend — Render

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 10000`
- **Environment Variables:** `OPENROUTER_API_KEY`, `GOOGLE_DRIVE_FOLDER_ID`
- **Secret File:** Upload `credentials.json` at path `/etc/secrets/credentials.json`

### Frontend — Streamlit Cloud

- Point to `frontend/app.py`
- Add secret: `BACKEND_URL = "https://drivescout-ai.onrender.com"`

---

## 🔍 Example Queries

| Query | What it does |
|---|---|
| `find pdf files` | Returns all PDFs in the Drive folder |
| `show me spreadsheets` | Returns all Excel/Sheets files |
| `find images` | Returns all image files |
| `search for reports` | Searches filenames containing "Report" |
| `find invoice documents` | Searches for files named "Invoice" |
| `hello` | AI greets and explains what it can do |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/files?search=&file_type=` | Direct Drive file listing |
| GET | `/ai-search?query=` | AI-parsed single search |
| POST | `/chat` | Conversational agent endpoint |

### POST `/chat` — Request Body

```json
{
  "message": "find pdf files",
  "history": [
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "Hi! How can I help?"}
  ]
}
```

### POST `/chat` — Response

```json
{
  "response": "Found 3 file(s):\n- Report_Q1.pdf\n- Annual_Report.pdf\n- Summary.pdf",
  "files": [
    {
      "id": "1abc...",
      "name": "Report_Q1.pdf",
      "mimeType": "application/pdf"
    }
  ]
}
```

---

## 💡 Challenges & Solutions

| Challenge | Solution |
|---|---|
| LLM returning inconsistent JSON | Strict system prompt with examples + JSON fence stripping |
| Groq API organization restriction | Switched to OpenRouter with `openrouter/free` auto-router |
| Gemini API quota exhaustion | Migrated to OpenRouter for reliability |
| Render deploy crash (empty query_builder.py) | Implemented full `parse_query()` function |
| Google credentials path on Render | Used Render Secret Files at `/etc/secrets/credentials.json` |

---

## 🔮 Future Improvements

- Conversational memory with LangGraph state management
- Full-text search inside documents (`fullText` Drive API query)
- File preview thumbnails
- Date-based filtering ("files from last week")
- Authentication and multi-user support
- Semantic/vector search with embeddings

---

## 👩‍💻 Author

**Tanya Bajpai**
GitHub: [tanyabajpai](https://github.com/tanyabajpai/DriveScout-AI)

---

## ⭐ If you found this useful, give it a star on GitHub!
