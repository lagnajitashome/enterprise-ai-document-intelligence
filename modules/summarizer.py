from modules.llm import get_llm


def summarize_document(prompt):
    """
    Generates a summary using Gemini.
    """

    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content