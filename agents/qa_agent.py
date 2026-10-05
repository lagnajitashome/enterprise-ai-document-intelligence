from modules.llm import get_llm

from modules.retrieval import (
    rewrite_question,
    retrieve_documents,
    build_qa_chain,
)

from modules.embeddings import load_vector_store


def qa_agent(state):
    """
    QA Agent

    Handles document-based question answering.

    Flow:

    User Question
          ↓
    Question Rewriting
          ↓
    FAISS Retrieval
          ↓
    Relevant Documents
          ↓
    QA Chain
          ↓
    Gemini
          ↓
    Answer + Sources
    """

    # --------------------------------------------------
    # 1. Get information from state
    # --------------------------------------------------

    question = state["question"]
    chat_history = state.get("chat_history", [])

    print("\n[QA Agent]")
    print(f"Question: {question}")

    # --------------------------------------------------
    # 2. Load Gemini LLM
    # --------------------------------------------------

    llm = get_llm()

    # --------------------------------------------------
    # 3. Rewrite follow-up question
    # --------------------------------------------------

    if chat_history:

        rewritten_question = rewrite_question(
            llm,
            question,
            chat_history
        )

    else:

        rewritten_question = question

    print(f"Rewritten question: {rewritten_question}")

    # --------------------------------------------------
    # 4. Load FAISS vector store
    # --------------------------------------------------

    vector_store = load_vector_store()

    # --------------------------------------------------
    # 5. Retrieve relevant documents
    # --------------------------------------------------

    documents = retrieve_documents(
        vector_store,
        rewritten_question,
        k=3
    )

    print(f"Retrieved documents: {len(documents)}")

    # --------------------------------------------------
    # 5A. DEBUG RETRIEVED DOCUMENTS
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("RETRIEVED DOCUMENTS")
    print("=" * 70)

    for i, document in enumerate(documents, start=1):

        print(f"\n--- Document {i} ---")

        print("\nMetadata:")
        print(document.metadata)

        print("\nContent:")
        print(document.page_content[:1500])

        print("\n" + "-" * 70)

    print("=" * 70)
    print()

    # --------------------------------------------------
    # 6. Build QA chain
    # --------------------------------------------------

    qa_chain = build_qa_chain(llm)

    # --------------------------------------------------
    # 7. Generate answer
    # --------------------------------------------------

    answer = qa_chain.invoke(
        {
            "context": documents,
            "input": rewritten_question
        }
    )

    # --------------------------------------------------
    # 8. Extract sources
    # --------------------------------------------------

    sources = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        if source not in sources:
            sources.append(source)

    # --------------------------------------------------
    # 9. Return updated LangGraph state
    # --------------------------------------------------

    return {
        "answer": answer,

        "context": [
            document.page_content
            for document in documents
        ],

        "sources": sources
    }