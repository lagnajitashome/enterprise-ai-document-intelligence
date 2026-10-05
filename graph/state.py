from typing import TypedDict, List, Any


class AgentState(TypedDict, total=False):

    # ========================================================
    # USER REQUEST
    # ========================================================

    question: str

    # ========================================================
    # SUPERVISOR DECISION
    # ========================================================

    intent: str

    # ========================================================
    # RETRIEVED DOCUMENT CONTEXT
    # ========================================================

    context: List[Any]

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    answer: str

    # ========================================================
    # CONVERSATION HISTORY
    # ========================================================

    chat_history: List[Any]

    # ========================================================
    # SOURCE DOCUMENTS
    # ========================================================

    sources: List[str]

    # ========================================================
    # DOCUMENT COMPARISON
    # ========================================================

    # Full text of the first document
    document1: str

    # Full text of the second document
    document2: str

    # Filename of the first document
    document1_name: str

    # Filename of the second document
    document2_name: str