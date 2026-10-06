# Enterprise AI Document Intelligence Platform

An AI-powered document intelligence platform that allows users to upload PDF documents, ask questions, generate summaries, create FAQs, and compare two documents.

The application uses a multi-agent architecture with **LangGraph**, **FastAPI**, **Streamlit**, **FAISS**, and **Google Gemini**.

##  Features

- 📄 PDF document upload and processing
- 💬 RAG-based document Question Answering
- 📝 AI-powered document summarization
- 🔍 Comparison of two PDF documents
- ❓ Automatic FAQ generation
- 🤖 Multi-agent routing using LangGraph
- 🔎 FAISS-based vector similarity search
- 📚 Source-aware document retrieval

##  Architecture

### Application Architecture

```mermaid
flowchart LR

    A[User]
    --> B[Streamlit UI]
    --> C[FastAPI Backend]
    --> D[LangGraph Supervisor]

    D --> E[QA Agent]
    D --> F[Summary Agent]
    D --> G[Comparison Agent]
    D --> H[FAQ Agent]

    E --> I[Response]
    F --> I
    G --> I
    H --> I

    I --> B
```

### RAG Pipeline

```mermaid
flowchart LR

    A[PDF Document]
    --> B[Text Extraction]
    --> C[Text Chunking]
    --> D[Gemini Embeddings]
    --> E[FAISS Vector Store]
    --> F[Relevant Document Chunks]
    --> G[Gemini LLM]
    --> H[Final Answer]
```
