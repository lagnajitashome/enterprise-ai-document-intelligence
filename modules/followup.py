FOLLOW_UP_KEYWORDS = [
    "first",
    "second",
    "third",
    "fourth",
    "it",
    "this",
    "that",
    "these",
    "those",
    "he",
    "she",
    "they",
    "them",
    "previous",
    "above",
    "last",
]


def is_follow_up(question):

    question = question.lower()

    return any(
        keyword in question
        for keyword in FOLLOW_UP_KEYWORDS
    )