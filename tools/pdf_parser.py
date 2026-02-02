import fitz
import os
import re
from typing import Dict


SECTION_HEADERS = {
    "abstract": r"(?:^|\n)\s*(abstract)\s*\n",
    "introduction": r"(?:^|\n)\s*(\d+\.?\s*)?introduction\s*\n",
    "method": r"(?:^|\n)\s*(\d+\.?\s*)?(method|approach|methodology)\s*\n",
    "experiments": r"(?:^|\n)\s*(\d+\.?\s*)?(experiment|evaluation|results)\s*\n",
    "discussion": r"(?:^|\n)\s*(\d+\.?\s*)?(discussion|analysis)\s*\n",
    "conclusion": r"(?:^|\n)\s*(\d+\.?\s*)?(conclusion|future work)\s*\n",
}


def parse_pdf_with_sections(file_path: str) -> Dict[str, str]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found: {file_path}")

    doc = fitz.open(file_path)
    full_text = "\n".join(page.get_text() for page in doc)
    doc.close()

    text = full_text.lower()
    matches = []

    for section, pattern in SECTION_HEADERS.items():
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            matches.append((m.start(), section))

    # Sort by appearance
    matches.sort(key=lambda x: x[0])

    sections: Dict[str, str] = {}

    for i, (start, name) in enumerate(matches):
        end = matches[i + 1][0] if i + 1 < len(matches) else len(full_text)
        sections[name] = full_text[start:end].strip()

    # 🔒 Always keep full text
    sections["full_text"] = full_text

    return sections