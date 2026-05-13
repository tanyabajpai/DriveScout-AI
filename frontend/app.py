import streamlit as st
from utils.api_client import search_files


st.set_page_config(
    page_title="DriveScout AI",
    page_icon="📁",
    layout="centered"
)


# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("📌 About")

    st.write(
        """
        DriveScout AI helps search
        Google Drive files using
        natural language queries.
        """
    )

    st.write("### Example Queries")

    st.write("- find reports")
    st.write("- show images")
    st.write("- find spreadsheets")


# ---------------- HELPERS ---------------- #

def format_file_type(mime):

    mime = mime.lower()

    if "pdf" in mime:
        return "PDF"

    elif "image" in mime:
        return "Image"

    elif "spreadsheet" in mime:
        return "Spreadsheet"

    elif "video" in mime:
        return "Video"

    return "Document"


# ---------------- UI ---------------- #

st.title("📁 DriveScout AI")

st.write(
    "Search Google Drive files using natural language."
)

st.caption(
    "Examples: find reports, show images, find spreadsheets"
)

user_input = st.text_input(
    "What would you like to find?",
    placeholder="Find pdf reports"
)


# ---------------- SEARCH ---------------- #

if st.button("Search"):

    if user_input:

        with st.spinner("Searching Drive..."):

            response = search_files(user_input)

        parsed_query = response["parsed_query"]

        search_term = parsed_query.get("search_term")
        file_type = parsed_query.get("file_type")

        # ---------- SUCCESS MESSAGE ---------- #

        if search_term:

            st.success(
                f"Searching for "
                f"{file_type or 'all'} files "
                f"related to '{search_term}'"
            )

        else:

            st.success(
                f"Searching for "
                f"{file_type or 'all'} files"
            )

        # ---------- FILE COUNT ---------- #

        st.subheader(
            f"Files Found: {response['total_files']}"
        )

        # ---------- FILE TYPE COUNTS ---------- #

        pdf_count = 0
        image_count = 0
        spreadsheet_count = 0
        video_count = 0

        for file in response["files"]:

            file_type_name = format_file_type(
                file["mimeType"]
            )

            if file_type_name == "PDF":
                pdf_count += 1

            elif file_type_name == "Image":
                image_count += 1

            elif file_type_name == "Spreadsheet":
                spreadsheet_count += 1

            elif file_type_name == "Video":
                video_count += 1

        # ---------- SUMMARY ---------- #

        with st.expander("📊 File Summary"):

            st.write(f"📄 PDFs: {pdf_count}")

            st.write(f"🖼 Images: {image_count}")

            st.write(
                f"📊 Spreadsheets: "
                f"{spreadsheet_count}"
            )

            st.write(f"🎥 Videos: {video_count}")

        # ---------- FILE RESULTS ---------- #

        if response["files"]:

            for file in response["files"]:

                file_link = (
                    f"https://drive.google.com/open?id={file['id']}"
                )

                with st.container(border=True):

                    st.write(
                        f"📄 Name: {file['name']}"
                    )

                    st.write(
                        f"📁 Type: "
                        f"{format_file_type(file['mimeType'])}"
                    )

                    st.link_button(
                        "🔗 Open in Drive",
                        file_link
                    )

        else:

            st.warning(
                "No matching files found."
            )