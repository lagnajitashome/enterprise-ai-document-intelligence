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

```mermaid
flowchart TD

    A[User] --> B[Streamlit UI]

    B --> C[FastAPI Backend]

    C --> D[LangGraph Supervisor]

    D -->|QA| E[QA Agent]
    D -->|Summary| F[Summary Agent]
    D -->|Comparison| G[Comparison Agent]
    D -->|FAQ| H[FAQ Agent]

    E --> I[FAISS Vector Store]
    F --> I
    H --> I

    I --> J[Gemini Embeddings]
    I --> K[Relevant Document Chunks]

    K --> E
    K --> F
    K --> H

    E --> L[Gemini LLM]
    F --> L
    G --> L
    H --> L

    L --> M[Final Response]

    M --> B
```
