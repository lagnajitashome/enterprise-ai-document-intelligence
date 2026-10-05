import streamlit as st


def initialize_memory():

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "last_context" not in st.session_state:
        st.session_state.last_context = ""

    if "last_documents" not in st.session_state:
        st.session_state.last_documents = []


def save_message(role, message):

    st.session_state.chat_history.append(
        {
            "role": role,
            "content": message
        }
    )


def get_chat_history():

    return st.session_state.chat_history


def clear_memory():

    st.session_state.chat_history = []
    st.session_state.last_context = ""


# -------------------------
# NEW FUNCTIONS
# -------------------------

def save_last_context(context):

    st.session_state.last_context = context


def get_last_context():

    return st.session_state.last_context
def save_last_documents(documents):
    st.session_state.last_documents = documents


def get_last_documents():
    return st.session_state.get("last_documents", [])