import fitz  # PyMuPDF
import os
import re
from typing import Dict


SECTION_HEADERS = {
    "abstract": r"\babstract\b",
    "introduction": r"\bintroduction\b",
    "method": r"\b(method|approach|methodology)\b",
    "experiments": r"\b(experiment|evaluation|results)\b",
    "discussion": r"\b(discussion|analysis)\b",
    "conclusion": r"\b(conclusion|future work)\b",
}


def parse_pdf_with_sections(file_path: str) -> Dict[str, str]:
    """
    Extract text from a PDF and split it into coarse sections.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"PDF file not found at path: {os.path.abspath(file_path)}"
        )

    doc = fitz.open(file_path)
    full_text = "\n".join(page.get_text() for page in doc)
    doc.close()

    lower = full_text.lower()
    sections: Dict[str, str] = {}
    indices = []

    for name, pattern in SECTION_HEADERS.items():
        match = re.search(pattern, lower)
        if match:
            indices.append((match.start(), name))

    # Sort sections by appearance
    indices.sort(key=lambda x: x[0])

    for i, (start_idx, name) in enumerate(indices):
        end_idx = indices[i + 1][0] if i + 1 < len(indices) else len(full_text)
        sections[name] = full_text[start_idx:end_idx].strip()

    # Fallback if nothing matched
    if not sections:
        sections["full_text"] = full_text

    return sections