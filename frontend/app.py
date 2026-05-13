import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "https://drivescout-ai.onrender.com")

st.set_page_config(
    page_title="DriveScout AI",
    page_icon="📁",
    layout="centered"
)

# --- Sidebar ---
with st.sidebar:
    st.title("📁 DriveScout AI")
    st.write("Search your Google Drive using natural language.")
    st.divider()
    st.write("**Try asking:**")
    st.write("- Find all PDF reports")
    st.write("- Show me spreadsheets")
    st.write("- Find images")
    st.write("- Search for invoices")
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.all_files = []
        st.rerun()

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "all_files" not in st.session_state:
    st.session_state.all_files = []

st.title("📁 DriveScout AI")
st.caption("Your Google Drive search assistant. Ask me anything!")

# --- Render chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("files"):
            for f in msg["files"]:
                link = f"https://drive.google.com/open?id={f['id']}"
                with st.container(border=True):
                    st.write(f"📄 **{f['name']}**")
                    st.caption(f"Type: {f['mimeType']}")
                    st.link_button("🔗 Open in Drive", link)

# --- Chat input ---
user_input = st.chat_input("Ask me to find files in your Drive...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Build history for backend (exclude files metadata)
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]
    ]

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Searching Drive..."):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": user_input, "history": history},
                    timeout=60
                )
                data = resp.json()

                ai_text = data.get("response", "Sorry, something went wrong.")
                files = data.get("files", [])

                st.write(ai_text)

                if files:
                    for f in files:
                        link = f"https://drive.google.com/open?id={f['id']}"
                        with st.container(border=True):
                            st.write(f"📄 **{f['name']}**")
                            st.caption(f"Type: {f['mimeType']}")
                            st.link_button("🔗 Open in Drive", link)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_text,
                    "files": files
                })

            except Exception as e:
                err = f"Connection error: {str(e)}"
                st.error(err)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": err,
                    "files": []
                })