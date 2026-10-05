from pypdf import PdfReader
from langchain_core.documents import Document


def get_pdf_text(pdf_docs):
    """
    Reads one or more uploaded PDF files.

    Returns:
        List[Document]

    Each Document contains:
        - page_content: extracted text
        - metadata:
            - source: PDF filename
            - page: page number
    """

    documents = []

    for pdf in pdf_docs:

        pdf_reader = PdfReader(pdf)

        for page_number, page in enumerate(pdf_reader.pages):

            extracted_text = page.extract_text()

            if extracted_text and extracted_text.strip():

                document = Document(
                    page_content=extracted_text,
                    metadata={
                        "source": pdf.name,
                        "page": page_number + 1
                    }
                )

                documents.append(document)

    return documents