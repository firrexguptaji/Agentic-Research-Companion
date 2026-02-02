import fitz  # PyMuPDF


def parse_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): Path to the PDF file

    Returns:
        str: Extracted text content
    """
    doc = fitz.open(file_path)
    text_chunks = []

    for page in doc:
        text_chunks.append(page.get_text())

    doc.close()
    return "\n".join(text_chunks)