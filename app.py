import streamlit as st
import requests

from modules.memory import (
    initialize_memory,
    save_message,
    get_chat_history,
    clear_memory
)


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Enterprise AI Document Intelligence",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

initialize_memory()

if "processed" not in st.session_state:
    st.session_state.processed = False

if "filename" not in st.session_state:
    st.session_state.filename = ""

if "upload_response" not in st.session_state:
    st.session_state.upload_response = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #666;
        margin-bottom: 25px;
    }

    .status-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f7ff;
        border: 1px solid #c9e2ff;
        margin-bottom: 15px;
    }

    .source-box {
        padding: 10px;
        border-radius: 8px;
        background-color: #f7f7f7;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📄 Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.write(
            f"**Selected:** {uploaded_file.name}"
        )

        if st.button(
            "⚙️ Process Document",
            use_container_width=True
        ):

            with st.spinner(
                "Uploading and processing document..."
            ):

                try:

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }

                    response = requests.post(
                        f"{API_URL}/documents/upload",
                        files=files,
                        timeout=180
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.session_state.processed = True
                        st.session_state.filename = uploaded_file.name
                        st.session_state.upload_response = result

                        st.success(
                            "Document processed successfully!"
                        )

                    else:

                        st.error(
                            f"Upload failed: {response.text}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to FastAPI. "
                        "Make sure the backend is running."
                    )

                except Exception as e:

                    st.error(
                        f"Error: {str(e)}"
                    )

    # --------------------------------------------------------
    # Document Status
    # --------------------------------------------------------

    if st.session_state.processed:

        st.markdown(
            """
            <div class="status-box">
            <b>✅ Document Ready</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            f"**File:** {st.session_state.filename}"
        )

        if st.session_state.upload_response:

            result = st.session_state.upload_response

            if "pages" in result:
                st.write(
                    f"📄 Pages: {result['pages']}"
                )

            if "chunks" in result:
                st.write(
                    f"🧩 Chunks: {result['chunks']}"
                )

    st.divider()

    # --------------------------------------------------------
    # Chat Memory
    # --------------------------------------------------------

    st.subheader("💬 Conversation")

    if st.button(
        "🗑️ Clear Chat History",
        use_container_width=True
    ):

        clear_memory()

        st.success("Chat history cleared.")

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Enterprise AI Document Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Multi-agent document intelligence using FastAPI, LangGraph, '
    'FAISS and Gemini.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TABS
# ============================================================

tab_qa, tab_summary, tab_comparison, tab_faq = st.tabs(
    [
        "💬 Ask Questions",
        "📝 Summary",
        "🔍 Comparison",
        "❓ FAQ Generator"
    ]
)


# ============================================================
# TAB 1 — QUESTION ANSWERING
# ============================================================

with tab_qa:

    st.subheader("Ask Questions About Your Document")

    if not st.session_state.processed:

        st.info(
            "Please upload and process a PDF from the sidebar first."
        )

    else:

        st.write(
            f"Currently loaded: **{st.session_state.filename}**"
        )

        question = st.text_input(
            "Enter your question",
            placeholder="Example: What technologies are used in this document?"
        )

        ask_button = st.button(
            "Ask Question",
            type="primary"
        )

        if ask_button:

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "Thinking..."
                ):

                    try:

                        response = requests.post(
                            f"{API_URL}/query",
                            json={
                                "question": question
                            },
                            timeout=180
                        )

                        if response.status_code == 200:

                            result = response.json()

                            answer = result.get(
                                "answer",
                                ""
                            )

                            intent = result.get(
                                "intent",
                                ""
                            )

                            sources = result.get(
                                "sources",
                                []
                            )

                            # Save conversation
                            save_message(
                                "user",
                                question
                            )

                            save_message(
                                "assistant",
                                answer
                            )

                            st.markdown("### Answer")

                            # Gemini may return either
                            # normal text or content blocks.
                            if isinstance(answer, list):

                                for block in answer:

                                    if isinstance(block, dict):

                                        st.markdown(
                                            block.get(
                                                "text",
                                                ""
                                            )
                                        )

                                    else:

                                        st.markdown(
                                            str(block)
                                        )

                            else:

                                st.markdown(
                                    str(answer)
                                )

                            # ------------------------------------------------
                            # Intent
                            # ------------------------------------------------

                            if intent:

                                st.caption(
                                    f"Agent selected: **{intent}**"
                                )

                            # ------------------------------------------------
                            # Sources
                            # ------------------------------------------------

                            if sources:

                                st.markdown(
                                    "### Sources"
                                )

                                for source in sources:

                                    st.markdown(
                                        f"- 📄 {source}"
                                    )

                        else:

                            st.error(
                                f"Query failed: {response.text}"
                            )

                    except requests.exceptions.ConnectionError:

                        st.error(
                            "Could not connect to FastAPI. "
                            "Make sure the backend is running."
                        )

                    except Exception as e:

                        st.error(
                            f"Error: {str(e)}"
                        )

        # --------------------------------------------------------
        # Conversation History
        # --------------------------------------------------------

        history = get_chat_history()

        if history:

            st.divider()

            st.subheader("Conversation History")

            for message in history:

                role = message.get(
                    "role",
                    ""
                )

                content = message.get(
                    "content",
                    ""
                )

                if role == "user":

                    st.markdown(
                        f"**You:** {content}"
                    )

                else:

                    st.markdown(
                        f"**AI:** {content}"
                    )


# ============================================================
# TAB 2 — SUMMARY
# ============================================================

with tab_summary:

    st.subheader("Document Summary")

    if not st.session_state.processed:

        st.info(
            "Please upload and process a PDF from the sidebar first."
        )

    else:

        st.write(
            f"Generate a summary of **{st.session_state.filename}**."
        )

        if st.button(
            "📝 Generate Summary",
            type="primary"
        ):

            with st.spinner(
                "Generating document summary..."
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/query",
                        json={
                            "question": "Summarize this document"
                        },
                        timeout=180
                    )

                    if response.status_code == 200:

                        result = response.json()

                        answer = result.get(
                            "answer",
                            ""
                        )

                        st.markdown(
                            "### Document Summary"
                        )

                        if isinstance(answer, list):

                            for block in answer:

                                if isinstance(block, dict):

                                    st.markdown(
                                        block.get(
                                            "text",
                                            ""
                                        )
                                    )

                                else:

                                    st.markdown(
                                        str(block)
                                    )

                        else:

                            st.markdown(
                                str(answer)
                            )

                    else:

                        st.error(
                            f"Summary failed: {response.text}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to FastAPI."
                    )

                except Exception as e:

                    st.error(
                        f"Error: {str(e)}"
                    )


# ============================================================
# TAB 3 — DOCUMENT COMPARISON
# ============================================================

with tab_comparison:

    st.subheader("Compare Two Documents")

    st.write(
        "Upload two PDF documents to generate an AI-powered comparison."
    )

    file1 = st.file_uploader(
        "Upload Document 1",
        type=["pdf"],
        key="comparison_file_1"
    )

    file2 = st.file_uploader(
        "Upload Document 2",
        type=["pdf"],
        key="comparison_file_2"
    )

    if file1 is not None:

        st.write(
            f"📄 Document 1: **{file1.name}**"
        )

    if file2 is not None:

        st.write(
            f"📄 Document 2: **{file2.name}**"
        )

    if st.button(
        "🔍 Compare Documents",
        type="primary"
    ):

        if file1 is None or file2 is None:

            st.warning(
                "Please upload both documents."
            )

        else:

            with st.spinner(
                "Comparing documents..."
            ):

                try:

                    files = {

                        "file1": (
                            file1.name,
                            file1.getvalue(),
                            "application/pdf"
                        ),

                        "file2": (
                            file2.name,
                            file2.getvalue(),
                            "application/pdf"
                        )
                    }

                    response = requests.post(
                        f"{API_URL}/documents/compare",
                        files=files,
                        timeout=180
                    )

                    if response.status_code == 200:

                        result = response.json()

                        answer = result.get(
                            "answer",
                            ""
                        )

                        st.markdown(
                            "### Comparison Report"
                        )

                        if isinstance(answer, list):

                            for block in answer:

                                if isinstance(block, dict):

                                    st.markdown(
                                        block.get(
                                            "text",
                                            ""
                                        )
                                    )

                                else:

                                    st.markdown(
                                        str(block)
                                    )

                        else:

                            st.markdown(
                                str(answer)
                            )

                        sources = result.get(
                            "sources",
                            []
                        )

                        if sources:

                            st.markdown(
                                "### Documents Compared"
                            )

                            for source in sources:

                                st.markdown(
                                    f"- 📄 {source}"
                                )

                    else:

                        st.error(
                            f"Comparison failed: {response.text}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to FastAPI."
                    )

                except Exception as e:

                    st.error(
                        f"Error: {str(e)}"
                    )


# ============================================================
# TAB 4 — FAQ GENERATOR
# ============================================================

with tab_faq:

    st.subheader("Frequently Asked Questions")

    if not st.session_state.processed:

        st.info(
            "Please upload and process a PDF from the sidebar first."
        )

    else:

        st.write(
            f"Generate 10 important FAQs from **{st.session_state.filename}**."
        )

        if st.button(
            "❓ Generate FAQs",
            type="primary"
        ):

            with st.spinner(
                "Generating FAQs..."
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/query",
                        json={
                            "question": "Generate 10 FAQs from this document"
                        },
                        timeout=180
                    )

                    if response.status_code == 200:

                        result = response.json()

                        answer = result.get(
                            "answer",
                            ""
                        )

                        st.markdown(
                            "### Frequently Asked Questions"
                        )

                        if isinstance(answer, list):

                            for block in answer:

                                if isinstance(block, dict):

                                    st.markdown(
                                        block.get(
                                            "text",
                                            ""
                                        )
                                    )

                                else:

                                    st.markdown(
                                        str(block)
                                    )

                        else:

                            st.markdown(
                                str(answer)
                            )

                    else:

                        st.error(
                            f"FAQ generation failed: {response.text}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to FastAPI."
                    )

                except Exception as e:

                    st.error(
                        f"Error: {str(e)}"
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Enterprise AI Document Intelligence Platform | "
    "FastAPI • LangGraph • FAISS • Gemini • Streamlit"
)