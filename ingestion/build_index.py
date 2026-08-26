from pathlib import Path
from pypdf import PdfReader
import json
import re

DATA_FOLDER = Path("data")
OUTPUT_FILE = Path("data/document_index.json")

DOCUMENT_METADATA = {
    "01_Support_Policy_v3_CURRENT.pdf": {
        "type": "support_policy",
        "status": "current",
        "authority": "general_policy",
        "account_id": None,
    },

    "02_Support_Policy_v2_DEPRECATED.pdf": {
        "type": "support_policy",
        "status": "deprecated",
        "authority": "deprecated",
        "account_id": None,
    },
    "03_Cancellation_and_Service_Credit_SOP_v4.pdf": {
        "type": "sop",
        "status": "current",
        "authority": "current_sop",
        "account_id": None,
    },

    "04_Product_Operations_Guide_and_Known_Issues.pdf": {
        "type": "product_documentation",
        "status": "current",
        "authority": "product_documentation",
        "account_id": None,
    },

    "05_Northstar_Logistics_Enterprise_Agreement.pdf": {
        "type": "customer_agreement",
        "status": "active",
        "authority": "customer_agreement",
        "account_id": "ACCT-001",
    },

    "06_LumenWorks_Service_Agreement.pdf": {
        "type": "customer_agreement",
        "status": "active",
        "authority": "customer_agreement",
        "account_id": "ACCT-002",
    },
}

def read_pdf(file_path):

    reader = PdfReader(file_path)

    text_content = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text_content += page_text + "\n"

    return clean_pdf_text(text_content)

def clean_pdf_text(text):

    # Convert PDF line breaks into spaces first
    text = text.replace("\n", " ")

    # Normalize multiple spaces
    text = " ".join(text.split())

    # Restore bullet points as separate lines
    text = text.replace(" ● ", "\n● ")

    # Restore numbered sections as separate lines
    import re
    text = re.sub(r"\s+(\d+\.)\s+", r"\n\1 ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n+", "\n", text)

    return text.strip()

def build_index():

    documents = []

    for pdf_file in DATA_FOLDER.glob("*.pdf"):

        text_content = read_pdf(pdf_file)

        metadata = DOCUMENT_METADATA.get(
            pdf_file.name,
            {}
        )

        document_entry = {
            "file_name": pdf_file.name,
            "text": text_content,
            **metadata
        }
        documents.append(document_entry)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            documents, 
            f, 
            indent=2,
            ensure_ascii=False
            ) 
      
    print(f"Indexed {len(documents)} documents.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_index()
