import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GET EMBEDDING MODEL
# ============================================================

def get_embeddings():
    """
    Returns the Gemini embedding model.
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. "
            "Please check your .env file."
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )

    return embeddings


# ============================================================
# CREATE FAISS VECTOR STORE
# ============================================================

def get_vector_store(documents):
    """
    Creates a FAISS vector database from LangChain
    Document objects.

    Metadata such as:
        - source
        - page

    is preserved inside FAISS.
    """

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    vector_store.save_local("vector_store")

    return vector_store


# ============================================================
# LOAD FAISS VECTOR STORE
# ============================================================

def load_vector_store():
    """
    Loads the previously saved FAISS vector database.
    """

    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        "vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store