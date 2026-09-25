from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS_DIR = Path(__file__).resolve().parent / "docs"


def load_policy_chunks() -> list[tuple[str, str]]:
    chunks: list[tuple[str, str]] = []
    for doc_path in sorted(DOCS_DIR.glob("*.md")):
        text = doc_path.read_text(encoding="utf-8")
        paragraphs = re.split(r"\n\s*\n+", text)
        for paragraph in paragraphs:
            cleaned = " ".join(paragraph.strip().split())
            if cleaned:
                chunks.append((doc_path.name, cleaned))
    return chunks


def build_retriever():
    chunks = load_policy_chunks()
    texts = [chunk for _, chunk in chunks]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix, chunks


def answer_question(question: str, top_k: int = 3) -> str:
    vectorizer, matrix, chunks = build_retriever()
    query_vector = vectorizer.transform([question])
    scores = cosine_similarity(query_vector, matrix).flatten()
    top_indexes = np.argsort(scores)[::-1][:top_k]

    if not np.any(scores[top_indexes] > 0):
        return "I could not find a clearly relevant Zepto policy passage for that question. Please check the policy documents in the support_assistant/docs directory."

    snippets = []
    for idx in top_indexes:
        source, text = chunks[idx]
        snippets.append(f"- Source: {source}\n  {text}")

    policy_context = "\n".join(snippets)
    answer = (
        "Based on the policy passages below, the best grounded answer is:\n\n"
        f"{policy_context}\n\n"
        "These excerpts are the current basis for the answer and should be treated as the source of truth for this policy query."
    )
    return answer


def main() -> None:
    questions = [
        "What is Zepto's return policy for delivered orders?",
        "How do you handle customer personal data and privacy?",
        "What are the delivery timelines and shipping expectations?",
    ]

    for question in questions:
        print(f"Question: {question}\n")
        print(answer_question(question))
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()
