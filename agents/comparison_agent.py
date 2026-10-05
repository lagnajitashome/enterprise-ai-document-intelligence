from modules.comparator import compare_documents


def comparison_agent(state):
    """
    Comparison Agent

    Compares two uploaded documents using Gemini.

    Expected state:
        document1 -> text of first document
        document2 -> text of second document
    """

    print("\n==============================")
    print("COMPARISON AGENT")
    print("==============================")

    try:

        # ----------------------------------------------------
        # Get documents from state
        # ----------------------------------------------------

        document1 = state.get("document1", "")
        document2 = state.get("document2", "")

        print(
            "Document 1 available:",
            bool(document1)
        )

        print(
            "Document 2 available:",
            bool(document2)
        )

        # ----------------------------------------------------
        # Validate documents
        # ----------------------------------------------------

        if not document1 or not document2:

            print("Two documents are required.")

            return {
                "answer": (
                    "Please provide two documents "
                    "to perform a comparison."
                ),
                "context": [],
                "sources": []
            }

        # ----------------------------------------------------
        # Compare documents
        # ----------------------------------------------------

        print("Comparing documents using Gemini...")

        answer = compare_documents(
            document1,
            document2
        )

        print("Comparison generated successfully.")

        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return {
            "answer": answer,
            "context": [
                document1,
                document2
            ],
            "sources": [
                state.get("document1_name", "Document 1"),
                state.get("document2_name", "Document 2")
            ]
        }

    except Exception as e:

        print("\nCOMPARISON AGENT ERROR")
        print(str(e))

        return {
            "answer": f"Comparison generation failed: {str(e)}",
            "context": [],
            "sources": []
        }