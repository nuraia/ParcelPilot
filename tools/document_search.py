import json

INDEX_FILE = "data/document_index.json"

def search_documents(query, account_id=None):

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    query_words = query.lower().split()

    results = []
    for document in documents:

        # Ignore deprecated documents
        if document.get("status") == "deprecated":
            continue

        # If an account is provided, prioritize the customer's agreement
        if (
            document.get("type") == "customer_agreement"
            and account_id is not None
            and document.get("account_id") != account_id
        ):
            continue

        text = document["text"].lower()

        score = 0

        for word in query_words:

            if word in text:
                score += 1

            if score > 0:
                results.append({
                    "file_name": document["file_name"],
                    "type": document.get("type"),
                    "status": document.get("status"),
                    "authority": document.get("authority"),
                    "account_id": document.get("account_id"),
                    "score": score,
                    "text": document["text"]
                })
    results.sort(key=lambda x: x["score"], reverse=True)

    return results

if __name__ == "__main__":

    results = search_documents(
        "cancellation fee",
        account_id="ACCT-001"
    )

    for result in results:

        print("\n" + "=" * 70)

        print("DOCUMENT:", result["file_name"])
        print("TYPE:", result["type"])
        print("AUTHORITY:", result["authority"])
        print("SCORE:", result["score"])

        print("\nTEXT PREVIEW:")
        print(result["text"][:1000])