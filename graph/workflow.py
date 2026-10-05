from langgraph.graph import StateGraph, START, END

from graph.state import AgentState

# ============================================================
# REAL SPECIALIZED AGENTS
# ============================================================

from agents.qa_agent import qa_agent
from agents.summary_agent import summary_agent
from agents.faq_agent import faq_agent
from agents.comparison_agent import comparison_agent

from modules.llm import get_llm


# ============================================================
# SUPERVISOR AGENT
# ============================================================

def supervisor(state: AgentState):
    """
    Supervisor Agent

    Determines which specialized agent should handle
    the user's request.

    Routing strategy:

    1. Rule-based detection for clear requests
    2. Gemini classification for ambiguous requests
    3. QA as final fallback
    """

    question = state["question"].strip()

    print("\n==============================")
    print("SUPERVISOR AGENT")
    print("==============================")

    print("User question:")
    print(question)

    question_lower = question.lower()


    # ========================================================
    # 1. FAQ DETECTION
    # ========================================================

    faq_keywords = [
        "faq",
        "faqs",
        "frequently asked questions",
        "generate questions and answers",
        "generate questions & answers",
        "create questions and answers",
        "create questions & answers",
        "generate questions",
        "create questions",
    ]

    if any(keyword in question_lower for keyword in faq_keywords):

        print("Supervisor decision: faq")

        return {
            "intent": "faq"
        }


    # ========================================================
    # 2. COMPARISON DETECTION
    # ========================================================

    comparison_keywords = [
        "compare",
        "comparison",
        "similarities",
        "differences",
        "difference between",
        "difference among",
    ]

    if any(keyword in question_lower for keyword in comparison_keywords):

        print("Supervisor decision: comparison")

        return {
            "intent": "comparison"
        }


    # ========================================================
    # 3. SUMMARY DETECTION
    # ========================================================

    summary_keywords = [
        "summarize",
        "summarise",
        "summary",
        "give me a summary",
        "provide a summary",
        "summarize this document",
        "summarise this document",
        "overview",
        "give me an overview",
        "key points",
        "main points",
        "brief explanation",
        "explain the document briefly",
    ]

    if any(keyword in question_lower for keyword in summary_keywords):

        print("Supervisor decision: summary")

        return {
            "intent": "summary"
        }


    # ========================================================
    # 4. GEMINI CLASSIFICATION
    # ========================================================

    print("No explicit intent detected.")
    print("Using Gemini for classification...")

    llm = get_llm()

    prompt = f"""
You are the supervisor of an enterprise document
intelligence platform.

Classify the user's request into exactly ONE category.

Available categories:

qa
summary
comparison
faq

Definitions:

QA:
Questions asking for specific factual information
from the document.

Examples:
- What technologies are used?
- Who is the author?
- When was the project developed?
- What is the objective?
- What components are used?

SUMMARY:
Requests to summarize or provide an overview.

Examples:
- Summarize the document.
- Give me an overview.
- What are the key points?
- Give me the main points.

COMPARISON:
Requests to compare two or more documents.

Examples:
- Compare these documents.
- Find similarities between the documents.
- Find differences.
- Compare document A and document B.

FAQ:
Requests to generate frequently asked questions
or multiple questions and answers from the document.

Examples:
- Generate FAQs.
- Create 10 FAQs.
- Generate frequently asked questions.
- Generate questions and answers from this document.

IMPORTANT:

Return ONLY one word:

qa
summary
comparison
faq

User request:

{question}
"""

    response = llm.invoke(prompt)


    # ========================================================
    # HANDLE GEMINI RESPONSE
    # ========================================================
    #
    # Newer Gemini models can sometimes return response.content
    # as a list of content blocks instead of a plain string.
    #
    # This handles both formats safely.
    # ========================================================

    if isinstance(response.content, list):

        intent = "".join(
            block.get("text", "")
            if isinstance(block, dict)
            else str(block)
            for block in response.content
        ).strip().lower()

    else:

        intent = str(response.content).strip().lower()


    print("Gemini supervisor decision:", intent)


    # ========================================================
    # 5. VALIDATE INTENT
    # ========================================================

    valid_intents = {
        "qa",
        "summary",
        "comparison",
        "faq"
    }

    if intent not in valid_intents:

        print("Invalid intent detected.")
        print("Defaulting to QA.")

        intent = "qa"


    return {
        "intent": intent
    }


# ============================================================
# ROUTER
# ============================================================

def route_request(state: AgentState):
    """
    Routes the request to the appropriate specialized agent.
    """

    intent = state.get("intent", "qa")

    print("\n==============================")
    print("ROUTING")
    print("==============================")

    print("Intent:", intent)

    return intent


# ============================================================
# CREATE LANGGRAPH
# ============================================================

builder = StateGraph(AgentState)


# ============================================================
# ADD AGENTS AS NODES
# ============================================================

builder.add_node(
    "supervisor",
    supervisor
)

builder.add_node(
    "qa_agent",
    qa_agent
)

builder.add_node(
    "summary_agent",
    summary_agent
)

builder.add_node(
    "comparison_agent",
    comparison_agent
)

builder.add_node(
    "faq_agent",
    faq_agent
)


# ============================================================
# START → SUPERVISOR
# ============================================================

builder.add_edge(
    START,
    "supervisor"
)


# ============================================================
# SUPERVISOR → SPECIALIZED AGENT
# ============================================================

builder.add_conditional_edges(
    "supervisor",
    route_request,
    {
        "qa": "qa_agent",
        "summary": "summary_agent",
        "comparison": "comparison_agent",
        "faq": "faq_agent"
    }
)


# ============================================================
# SPECIALIZED AGENTS → END
# ============================================================

builder.add_edge(
    "qa_agent",
    END
)

builder.add_edge(
    "summary_agent",
    END
)

builder.add_edge(
    "comparison_agent",
    END
)

builder.add_edge(
    "faq_agent",
    END
)


# ============================================================
# COMPILE GRAPH
# ============================================================

graph = builder.compile()