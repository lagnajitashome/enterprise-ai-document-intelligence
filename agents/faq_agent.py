from modules.embeddings import load_vector_store
from modules.faq_generator import generate_faq


def faq_agent(state):
    """
    FAQ Agent

    Loads document chunks from FAISS and generates
    10 Frequently Asked Questions using Gemini.
    """

    print("\n==============================")
    print("FAQ AGENT")
    print("==============================")

    try:

        # ====================================================
        # LOAD FAISS VECTOR STORE
        # ====================================================

        vector_store = load_vector_store()

        print("FAISS vector store loaded.")

        # ====================================================
        # GET DOCUMENT CHUNKS
        # ====================================================

        documents = list(
            vector_store.docstore._dict.values()
        )

        print(
            "Number of document chunks:",
            len(documents)
        )

        # ====================================================
        # CHECK DOCUMENT AVAILABILITY
        # ====================================================

        if not documents:

            return {
                "answer": "No document content is available for FAQ generation.",
                "context": [],
                "sources": []
            }

        # ====================================================
        # COMBINE DOCUMENT CONTENT
        # ====================================================

        document_text = "\n\n".join(
            document.page_content
            for document in documents
        )

        # ====================================================
        # GENERATE FAQs
        # ====================================================

        answer = generate_faq(
            document_text
        )

        # ====================================================
        # EXTRACT SOURCES
        # ====================================================

        sources = []

        for document in documents:

            source = document.metadata.get(
                "source",
                "Unknown source"
            )

            if source not in sources:
                sources.append(source)

        print("FAQ generation completed successfully.")

        # ====================================================
        # RETURN AGENT STATE
        # ====================================================

        return {
            "answer": answer,

            "context": [
                document.page_content
                for document in documents
            ],

            "sources": sources
        }

    except Exception as e:

        print("\nFAQ AGENT ERROR")
        print(str(e))

        return {
            "answer": f"FAQ generation failed: {str(e)}",
            "context": [],
            "sources": []
        }