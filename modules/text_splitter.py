from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def get_text_chunks(documents):

    """
    Splits documents into smaller chunks.

    Accepts either:
    - LangChain Document objects
    - strings

    When Document objects are provided, metadata is preserved.
    """

    # --------------------------------------------------
    # Make sure input is a list
    # --------------------------------------------------

    if not isinstance(documents, list):
        documents = [documents]

    # --------------------------------------------------
    # If strings are passed, convert them to Documents
    # --------------------------------------------------

    if documents and isinstance(documents[0], str):

        documents = [
            Document(
                page_content=text,
                metadata={}
            )
            for text in documents
        ]

    # --------------------------------------------------
    # Split documents
    # --------------------------------------------------

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(
        documents
    )

    return chunks