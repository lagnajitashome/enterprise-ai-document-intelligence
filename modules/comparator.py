from modules.llm import get_llm


def compare_documents(document1, document2):
    """
    Compares two documents using Gemini.
    """

    llm = get_llm()

    prompt = f"""
You are an expert document comparison assistant.

Compare the following two documents.

Generate a professional comparison report.

Include:

1. Executive Summary

2. Similarities

3. Differences

4. Skills Comparison

5. Experience Comparison

6. Education Comparison

7. Strengths of Document 1

8. Strengths of Document 2

9. Final Recommendation

-------------------------
DOCUMENT 1
-------------------------

{document1}

-------------------------
DOCUMENT 2
-------------------------

{document2}

Use only the information available in the documents.

Return the result in clean markdown.
"""

    response = llm.invoke(prompt)

    return response.content