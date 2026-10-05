import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables from .env
load_dotenv()


def get_llm():
    """
    Returns the Gemini LLM used across the application.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    return llm