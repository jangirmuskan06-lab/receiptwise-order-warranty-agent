import re

from langchain_ollama import ChatOllama

from tools import calculate_return_warranty_window, lookup_order_status


def create_proactive_summary(items: list[dict]) -> list[dict]:
    """Automatically calculates return and warranty windows after upload."""
    summary = []

    for item in items:
        return_window = calculate_return_warranty_window.invoke({
            "item_name": item["name"],
            "category": item["category"],
            "purchase_date": item["purchase_date"],
            "window_type": "return",
        })

        warranty_window = calculate_return_warranty_window.invoke({
            "item_name": item["name"],
            "category": item["category"],
            "purchase_date": item["purchase_date"],
            "window_type": "warranty",
        })

        summary.append({
            "item": item,
            "return_window": return_window,
            "warranty_window": warranty_window,
        })

    return summary


def run_receipt_agent(question: str, retriever) -> dict:
    """
    Orchestrates grounded retrieval and, when an order ID is present,
    the live order-status lookup tool.
    """

    question_upper = question.upper()
    order_match = re.search(r"\bORD-\d+\b", question_upper)

    retrieval_words = [
        "return", "warranty", "policy", "receipt", "jacket",
        "earbuds", "item", "purchase", "eligible",
    ]

    needs_retrieval = (
        order_match is None
        or any(word in question.lower() for word in retrieval_words)
    )

    evidence = []
    actions = []
    answer_sections = []

    if needs_retrieval:
        documents = retriever.invoke(question)

        if documents:
            context = "\n\n".join(
                f"Source: {document.metadata['source']}\n"
                f"{document.page_content}"
                for document in documents
            )

            for document in documents:
                evidence.append({
                    "source": document.metadata.get(
                        "source",
                        "unknown source"
                    ).replace("_", " ").title(),
                    "content": document.page_content.strip(),
                })

            llm = ChatOllama(model="llama3.2", temperature=0)

            prompt = f"""
You are a careful retail order and warranty assistant.

Answer only the receipt, return-policy, or warranty part of the shopper's
question using the supplied context. Never invent products, prices, policy
terms, dates, or eligibility conditions.

If the answer is missing from the context, reply exactly:
I couldn't find that in your receipt or store policy.

Context:
{context}

Shopper question:
{question}
"""

            response = llm.invoke(prompt)

            answer_sections.append(
                "### Receipt and policy answer\n"
                + response.content.strip()
            )

            actions.append("Retrieved matching receipt and policy evidence")

        elif order_match is None:
            answer_sections.append(
                "I couldn't find that in your receipt or store policy."
            )

    if order_match:
        order_id = order_match.group(0)

        order_result = lookup_order_status.invoke({
            "order_id": order_id
        })

        actions.append(f"Ran live order-status lookup for {order_id}")

        if order_result["found"]:
            order_answer = (
                f"Order **{order_result['order_id']}** is currently "
                f"**{order_result['status']}**.\n\n"
                f"Tracking number: {order_result['tracking_number']}\n\n"
                f"Estimated delivery: {order_result['estimated_delivery']}"
            )

            evidence.append({
                "source": "Live Mock Order Database",
                "content": (
                    f"Order ID: {order_result['order_id']}\n"
                    f"Status: {order_result['status']}\n"
                    f"Tracking number: {order_result['tracking_number']}\n"
                    f"Estimated delivery: "
                    f"{order_result['estimated_delivery']}"
                ),
            })
        else:
            order_answer = order_result["message"]

        answer_sections.append("### Live order status\n" + order_answer)

    if not answer_sections:
        answer_sections.append(
            "I couldn't find that in your receipt or store policy."
        )

    return {
        "answer": "\n\n".join(answer_sections),
        "evidence": evidence,
        "actions": actions,
    }


def answer_followup_question(question: str, retriever) -> str:
    """Returns only the final grounded agent answer."""
    return run_receipt_agent(question, retriever)["answer"]


def answer_followup_with_evidence(question: str, retriever) -> dict:
    """Returns answer, sources, and agent actions for the app."""
    return run_receipt_agent(question, retriever)