# 📁 DriveScout AI

AI-powered Google Drive Search Assistant built using FastAPI, Streamlit, LangChain, Groq, and Google Drive API.

---

# 🚀 Overview

DriveScout AI allows users to search Google Drive files using natural language queries.

Instead of manually navigating folders, users can type queries like:

- find pdf reports
- show images
- find spreadsheets

The application uses AI to understand user intent, convert it into structured search parameters, and retrieve matching files from Google Drive.

---

# ✨ Features

- Natural language search
- AI-powered query parsing
- Google Drive API integration
- PDF filtering
- Image filtering
- Spreadsheet filtering
- Streamlit frontend
- FastAPI backend
- LangChain + Groq integration
- Dynamic Google Drive file retrieval
- File type detection
- Direct Google Drive file opening

---

# 🏗️ System Architecture

```text
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
LangChain + Groq LLM
        ↓
Google Drive API
```

---

# 🧠 How It Works

1. User enters a natural language query in Streamlit UI.
2. Frontend sends the query to FastAPI backend.
3. LangChain + Groq parses the query into structured JSON.
4. Backend converts structured data into Google Drive API filters.
5. Matching files are fetched and returned.
6. Results are displayed with direct Drive links.

---

# 🛠️ Tech Stack

## Frontend
- Streamlit

## Backend
- FastAPI
- Python

## AI Layer
- LangChain
- Groq LLM

## Cloud Integration
- Google Drive API

---

# 📸 Screenshots

## Home Page

![alt text](<Screenshot 2026-05-13 181500.png>)

---

## PDF Search Results

![alt text](<Screenshot 2026-05-13 181622-1.png>) ![alt text](<Screenshot 2026-05-13 181617-1.png>)

---

## Image Search Results

![alt text](<Screenshot 2026-05-13 181647-1.png>)

---

## Spreadsheet Search Results

![alt text](<Screenshot 2026-05-13 181711.png>)

---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

---

## 2. Navigate Into Project

```bash
cd DriveScout-AI
```

---

## 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file inside the backend folder.

Example:

```env
GROQ_API_KEY=your_groq_api_key
FOLDER_ID=your_google_drive_folder_id
```

---

## 5. Add Google Drive Credentials

Place your Google Cloud service account credentials file inside:

```text
backend/app/config/credentials.json
```

---

## 6. Run FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

## 7. Run Streamlit Frontend

Open another terminal:

```bash
cd frontend
streamlit run app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# 🔍 Example Queries

- find reports
- find pdf reports
- show images
- find spreadsheets
- show videos

---

# 📂 Project Structure

```text
DriveScout-AI/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── config/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tools/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── utils/
│   └── app.py
│
├── README.md
└── .gitignore
```

---

# 💡 Challenges Faced

- Handling Google Drive permissions
- MIME-type based filtering
- AI query parsing consistency
- Backend-frontend integration
- Managing FastAPI async responses

---

# 🔮 Future Improvements

- Conversational memory
- Multi-turn AI search
- Authentication system
- File previews
- Multi-user support
- Deployment on cloud platforms
- Semantic document search

---

# 🌐 Deployment Ideas

## Backend
- Render
- Railway

## Frontend
- Streamlit Cloud

---

# 📈 Resume-Worthy Highlights

- Built a modular AI-powered full-stack application
- Integrated LLM orchestration with cloud storage APIs
- Designed natural language to structured query conversion
- Implemented intelligent MIME-type filtering system

---

# 📄 Resume Description

Built an AI-powered Google Drive search assistant using FastAPI, Streamlit, LangChain, Groq LLM, and Google Drive API with natural language query parsing and intelligent file retrieval.

Designed a modular full-stack architecture integrating conversational AI orchestration, MIME-type filtering, and dynamic cloud file search capabilities.

---

# 👩‍💻 Author

Tanya Bajpai

---

# ⭐ If You Like This Project

Give it a star on GitHub ⭐
