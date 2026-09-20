import re
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def parse_receipt(receipt_text: str):
    """Extract the order ID, purchase date, and each purchased item."""

    order_match = re.search(r"Order ID:\s*(.+)", receipt_text, re.IGNORECASE)
    date_match = re.search(r"Purchase Date:\s*(.+)", receipt_text, re.IGNORECASE)

    if not order_match or not date_match:
        raise ValueError(
            "Receipt must contain an Order ID and a Purchase Date."
        )

    order_id = order_match.group(1).strip()
    purchase_date = date_match.group(1).strip()

    item_pattern = (
        r"^\s*\d+\.\s*"
        r"(?P<name>[^|\n]+)\|\s*"
        r"Category:\s*(?P<category>[^|\n]+)\|\s*"
        r"Price:\s*(?P<price>[^\n]+)$"
    )

    items = []

    for match in re.finditer(item_pattern, receipt_text, re.MULTILINE | re.IGNORECASE):
        items.append({
            "name": match.group("name").strip(),
            "category": match.group("category").strip(),
            "price": match.group("price").strip(),
            "order_id": order_id,
            "purchase_date": purchase_date,
        })

    if not items:
        raise ValueError(
            "No items were found. Use the required receipt item format."
        )

    return order_id, purchase_date, items


def build_receipt_retriever(receipt_text: str, policy_text: str):
    """
    Creates one Chroma database per uploaded order.
    Every receipt item is its own chunk; policy text is split separately.
    """

    order_id, purchase_date, items = parse_receipt(receipt_text)

    receipt_documents = []

    for item in items:
        receipt_documents.append(
            Document(
                page_content=(
                    f"Purchased item: {item['name']}\n"
                    f"Category: {item['category']}\n"
                    f"Price: {item['price']}\n"
                    f"Purchase date: {item['purchase_date']}\n"
                    f"Order ID: {item['order_id']}"
                ),
                metadata={
                    "source": "shopper_receipt",
                    "order_id": order_id,
                    "item_name": item["name"],
                },
            )
        )

    policy_splitter = RecursiveCharacterTextSplitter(
        chunk_size=350,
        chunk_overlap=40,
    )

    policy_documents = policy_splitter.create_documents(
        [policy_text],
        metadatas=[{
            "source": "store_policy",
            "order_id": order_id,
        }],
    )

    all_documents = receipt_documents + policy_documents

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = Chroma.from_documents(
        documents=all_documents,
        embedding=embeddings,
        collection_name=f"receipt_{order_id}",
        persist_directory=f"chroma_db/{order_id}",
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    return retriever, items, order_id


if __name__ == "__main__":
    receipt_text = Path("data/sample-receipt.txt").read_text(encoding="utf-8")
    policy_text = Path("data/policy.txt").read_text(encoding="utf-8")

    retriever, items, order_id = build_receipt_retriever(
        receipt_text,
        policy_text,
    )

    print(f"Receipt indexed successfully for order: {order_id}")
    print("\nItems found:")

    for item in items:
        print(f"- {item['name']} ({item['category']})")

    print("\nRetriever test: when can I return the jacket?\n")

    results = retriever.invoke("When can I return the jacket?")

    for number, document in enumerate(results, start=1):
        print(f"Result {number} | Source: {document.metadata['source']}")
        print(document.page_content)
        print("-" * 50)