from modules.embeddings import load_vector_store
from modules.summarizer import summarize_document


def summary_agent(state):
    """
    Summary Agent

    Loads document chunks from FAISS
    and generates a summary using Gemini.
    """

    print("\n==============================")
    print("SUMMARY AGENT")
    print("==============================")

    try:

        # Load FAISS vector store
        vector_store = load_vector_store()

        print("FAISS vector store loaded.")

        # Get all documents stored in FAISS
        documents = list(
            vector_store.docstore._dict.values()
        )

        print(
            "Number of document chunks:",
            len(documents)
        )

        if not documents:

            return {
                "answer": "No document content is available for summarization.",
                "context": [],
                "sources": []
            }

        # Combine all document chunks
        document_text = "\n\n".join(
            document.page_content
            for document in documents
        )

        # Create prompt
        prompt = f"""
You are an enterprise document summarization agent.

Summarize the following document.

Requirements:

1. Identify the main topic of the document.
2. Explain the main objective or purpose.
3. Identify important concepts, technologies,
   methods, or findings.
4. Include important details when relevant.
5. Do not invent information.
6. Use only the provided document content.
7. Keep the summary clear and professional.
8. Use bullet points where appropriate.

DOCUMENT CONTENT:

{document_text}

Provide a concise but informative summary.
"""

        # Generate summary
        answer = summarize_document(prompt)

        # Extract sources
        sources = []

        for document in documents:

            source = document.metadata.get(
                "source",
                "Unknown source"
            )

            if source not in sources:
                sources.append(source)

        print("Summary generated successfully.")

        return {
            "answer": answer,
            "context": [
                document.page_content
                for document in documents
            ],
            "sources": sources
        }

    except Exception as e:

        print("\nSUMMARY AGENT ERROR")
        print(str(e))

        return {
            "answer": f"Summary generation failed: {str(e)}",
            "context": [],
            "sources": []
        }