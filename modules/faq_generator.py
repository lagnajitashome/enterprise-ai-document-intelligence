from modules.llm import get_llm


def generate_faq(document_text):
    """
    Generates Frequently Asked Questions from the uploaded document.
    """

    llm = get_llm()

    prompt = f"""
You are an expert document analyst.

Read the following document carefully.

Generate the 10 most important Frequently Asked Questions (FAQs)
along with concise and accurate answers.

Requirements:

- Questions should be meaningful.
- Answers should come ONLY from the document.
- Do not invent information.
- Format the output exactly as follows.

# Frequently Asked Questions

## Q1:
Answer...

## Q2:
Answer...

Continue until Q10.

Document:

{document_text}
"""

    response = llm.invoke(prompt)

    return response.content