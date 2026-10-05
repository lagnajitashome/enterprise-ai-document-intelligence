from fastapi import FastAPI, UploadFile, File, HTTPException
from io import BytesIO
from typing import List

from pypdf import PdfReader

from langchain_core.documents import Document

from pydantic import BaseModel

from modules.text_splitter import get_text_chunks
from modules.embeddings import get_vector_store

from graph.workflow import graph


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Enterprise Document Intelligence API",
    description="Backend API for the multi-agent document intelligence platform",
    version="1.0.0"
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def extract_pdf_documents(file_bytes, filename):
    """
    Extracts text from a PDF and returns LangChain
    Document objects with source and page metadata.
    """

    reader = PdfReader(
        BytesIO(file_bytes)
    )

    documents = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text and text.strip():

            document = Document(
                page_content=text,
                metadata={
                    "source": filename,
                    "page": page_number
                }
            )

            documents.append(document)

    return reader, documents


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Enterprise Document Intelligence API"
    }


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # Check file type
    # --------------------------------------------------------

    if file.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # --------------------------------------------------------
    # Read PDF
    # --------------------------------------------------------

    try:

        file_bytes = await file.read()

        reader, documents = extract_pdf_documents(
            file_bytes,
            file.filename
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Could not read PDF: {str(e)}"
        )

    # --------------------------------------------------------
    # Check extracted text
    # --------------------------------------------------------

    if not documents:

        raise HTTPException(
            status_code=400,
            detail="No readable text found in the PDF."
        )

    # --------------------------------------------------------
    # DEBUG DOCUMENTS
    # --------------------------------------------------------

    print("\n==============================")
    print("DOCUMENT DEBUG")
    print("==============================")

    print(
        "Number of documents:",
        len(documents)
    )

    print(
        "Type of first document:",
        type(documents[0])
    )

    print(
        "Metadata:",
        documents[0].metadata
    )

    print("==============================\n")

    # --------------------------------------------------------
    # Split documents into chunks
    # --------------------------------------------------------

    try:

        text_chunks = get_text_chunks(
            documents
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Text chunking failed: {str(e)}"
        )

    # --------------------------------------------------------
    # DEBUG CHUNKS
    # --------------------------------------------------------

    print("\n==============================")
    print("CHUNK DEBUG")
    print("==============================")

    print(
        "Number of chunks:",
        len(text_chunks)
    )

    print(
        "Type of first chunk:",
        type(text_chunks[0])
    )

    print(
        "Chunk metadata:",
        text_chunks[0].metadata
    )

    print("==============================\n")

    # --------------------------------------------------------
    # Create FAISS vector store
    # --------------------------------------------------------

    try:

        get_vector_store(
            text_chunks
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"FAISS vector store creation failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {

        "message": "Document processed successfully",

        "filename": file.filename,

        "content_type": file.content_type,

        "pages": len(reader.pages),

        "text_pages": len(documents),

        "chunks": len(text_chunks),

        "vector_store": "FAISS",

        "status": "ready"
    }


# ============================================================
# DOCUMENT COMPARISON
# ============================================================

@app.post("/documents/compare")
async def compare_documents_endpoint(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):

    print("\n==============================")
    print("DOCUMENT COMPARISON REQUEST")
    print("==============================")

    # --------------------------------------------------------
    # Validate file types
    # --------------------------------------------------------

    if file1.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Document 1 must be a PDF."
        )

    if file2.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Document 2 must be a PDF."
        )

    # --------------------------------------------------------
    # Read both PDFs
    # --------------------------------------------------------

    try:

        file1_bytes = await file1.read()
        file2_bytes = await file2.read()

        reader1, documents1 = extract_pdf_documents(
            file1_bytes,
            file1.filename
        )

        reader2, documents2 = extract_pdf_documents(
            file2_bytes,
            file2.filename
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Could not read comparison documents: {str(e)}"
        )

    # --------------------------------------------------------
    # Validate extracted text
    # --------------------------------------------------------

    if not documents1:

        raise HTTPException(
            status_code=400,
            detail=f"No readable text found in {file1.filename}."
        )

    if not documents2:

        raise HTTPException(
            status_code=400,
            detail=f"No readable text found in {file2.filename}."
        )

    # --------------------------------------------------------
    # Combine pages into full document text
    # --------------------------------------------------------

    document1_text = "\n\n".join(
        document.page_content
        for document in documents1
    )

    document2_text = "\n\n".join(
        document.page_content
        for document in documents2
    )

    print(
        "Document 1:",
        file1.filename
    )

    print(
        "Document 2:",
        file2.filename
    )

    print(
        "Document 1 pages:",
        len(documents1)
    )

    print(
        "Document 2 pages:",
        len(documents2)
    )

    # --------------------------------------------------------
    # Create LangGraph state
    # --------------------------------------------------------

    initial_state = {

        "question": (
            f"Compare {file1.filename} "
            f"and {file2.filename}"
        ),

        "context": [],

        "intent": "",

        "answer": "",

        "chat_history": [],

        "sources": [],

        "document1": document1_text,

        "document2": document2_text,

        "document1_name": file1.filename,

        "document2_name": file2.filename
    }

    # --------------------------------------------------------
    # Run LangGraph
    # --------------------------------------------------------

    try:

        result = graph.invoke(
            initial_state
        )

    except Exception as e:

        print("\n==============================")
        print("COMPARISON ERROR")
        print("==============================")

        print(str(e))

        print("==============================\n")

        raise HTTPException(
            status_code=500,
            detail=f"Comparison processing failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Return comparison result
    # --------------------------------------------------------

    return {

        "document1": file1.filename,

        "document2": file2.filename,

        "intent": result.get(
            "intent",
            "comparison"
        ),

        "answer": result.get(
            "answer",
            ""
        ),

        "sources": result.get(
            "sources",
            [
                file1.filename,
                file2.filename
            ]
        )
    }


# ============================================================
# QUERY REQUEST MODEL
# ============================================================

class QueryRequest(BaseModel):

    question: str


# ============================================================
# QUERY ENDPOINT
# ============================================================

@app.post("/query")
async def query_documents(
    request: QueryRequest
):

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        # ----------------------------------------------------
        # Create initial LangGraph state
        # ----------------------------------------------------

        initial_state = {

            "question": request.question,

            "context": [],

            "intent": "",

            "answer": "",

            "chat_history": [],

            "sources": []
        }

        # ----------------------------------------------------
        # Run LangGraph
        # ----------------------------------------------------

        result = graph.invoke(
            initial_state
        )

        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return {

            "question": request.question,

            "intent": result.get(
                "intent",
                ""
            ),

            "answer": result.get(
                "answer",
                ""
            ),

            "sources": result.get(
                "sources",
                []
            )
        }

    except Exception as e:

        print("\n==============================")
        print("QUERY ERROR")
        print("==============================")

        print(str(e))

        print("==============================\n")

        raise HTTPException(
            status_code=500,
            detail=f"Query processing failed: {str(e)}"
        )