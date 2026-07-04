import re
from io import BytesIO

import streamlit as st

from config import SUMMARY_CHUNK_CHARS, SUMMARY_CHUNK_OVERLAP


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def read_pdf_text_from_bytes(file_bytes: bytes) -> tuple[str, int]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Missing pypdf. Install it with: pip install pypdf") from exc

    reader = PdfReader(BytesIO(file_bytes))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = clean_text(page.extract_text() or "")
        if page_text:
            pages.append(f"[Page {page_number}]\n{page_text}")

    return "\n\n".join(pages).strip(), len(reader.pages)


def trim_text_to_limit(text: str, char_limit: int) -> str:
    if len(text) <= char_limit:
        return text.strip()

    trimmed = text[:char_limit].rsplit(" ", 1)[0].strip()
    return f"{trimmed}..."


def split_long_paragraph(paragraph: str, chunk_chars: int) -> list[str]:
    if len(paragraph) <= chunk_chars:
        return [paragraph]
    return [piece.strip() for piece in re.split(r"(?<=[.!?])\s+", paragraph) if piece.strip()]


def split_text_into_chunks(
    text: str,
    chunk_chars: int = SUMMARY_CHUNK_CHARS,
    overlap_chars: int = SUMMARY_CHUNK_OVERLAP,
) -> list[str]:
    text = clean_text(text)
    if not text:
        return []

    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    base_chunks, current = [], ""

    for paragraph in paragraphs:
        for piece in split_long_paragraph(paragraph, chunk_chars):
            candidate = f"{current}\n\n{piece}".strip() if current else piece

            if current and len(candidate) > chunk_chars:
                base_chunks.append(trim_text_to_limit(current, chunk_chars))
                current = piece
            else:
                current = candidate

    if current:
        base_chunks.append(trim_text_to_limit(current, chunk_chars))

    if overlap_chars <= 0 or len(base_chunks) <= 1:
        return base_chunks

    overlapped_chunks = [base_chunks[0]]
    for index, chunk in enumerate(base_chunks[1:], start=1):
        previous_tail = base_chunks[index - 1][-overlap_chars:].strip()
        overlapped = f"Previous context:\n{previous_tail}\n\nCurrent fragment:\n{chunk}".strip()
        overlapped_chunks.append(trim_text_to_limit(overlapped, chunk_chars + overlap_chars + 80))

    return overlapped_chunks
