from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from modules.prompts import (
    history_aware_prompt,
    qa_prompt,
)


def rewrite_question(llm, user_question, chat_history):
    """
    Rewrite a follow-up question into a standalone question.
    """

    chain = (
        RunnablePassthrough()
        | history_aware_prompt
        | llm
        | StrOutputParser()
    )

    rewritten_question = chain.invoke(
        {
            "input": user_question,
            "chat_history": chat_history
        }
    )

    return rewritten_question


def retrieve_documents(vector_store, question, k=3):
    """
    Retrieve relevant documents from FAISS.
    """

    retriever = vector_store.as_retriever(
        search_kwargs={"k": k}
    )

    documents = retriever.invoke(question)

    return documents


def build_qa_chain(llm):
    """
    Build the LangChain QA chain.
    """

    qa_chain = create_stuff_documents_chain(
        llm,
        qa_prompt
    )

    return qa_chain