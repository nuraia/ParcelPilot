from pathlib import Path
from pypdf import PdfReader

DATA_FOLDER = Path("data")

def read_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":

    pdf_files = list(DATA_FOLDER.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files in '{DATA_FOLDER}'.")

    for pdf_file in pdf_files:

        print(f"\n" + "=" * 70)
        print(pdf_file.name)
        print(f"\n" + "=" * 70)

        content = read_pdf(pdf_file)


        print(f"Characters extracted: {len(content)}")
        print(content[:500])