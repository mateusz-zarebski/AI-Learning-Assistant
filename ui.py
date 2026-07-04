import hashlib
import time

import streamlit as st

from config import (
    DEFAULT_MODEL_LABEL,
    EMBEDDING_MODEL_NAME,
    MODEL_OPTIONS,
    OUTPUT_STATE_DEFAULTS,
    QA_TOP_K,
    SUMMARY_CHUNK_CHARS,
    SUMMARY_CHUNK_OVERLAP,
)
from gemini_utils import get_api_key
from pdf_utils import read_pdf_text_from_bytes, split_text_into_chunks


def init_output_state() -> None:
    for key, default_value in OUTPUT_STATE_DEFAULTS.items():
        st.session_state.setdefault(key, default_value)


def clear_output_state() -> None:
    for key, default_value in OUTPUT_STATE_DEFAULTS.items():
        st.session_state[key] = default_value


def reset_outputs_when_pdf_changes(file_bytes: bytes) -> None:
    current_hash = hashlib.md5(file_bytes).hexdigest()

    if st.session_state.get("active_pdf_hash") != current_hash:
        st.session_state.active_pdf_hash = current_hash
        clear_output_state()

        # Reset old quiz checkbox selections when a new document is uploaded.
        for key in list(st.session_state.keys()):
            if key.startswith("quiz_chunk_"):
                del st.session_state[key]


def render_sidebar() -> tuple[str, str | None]:
    with st.sidebar:
        st.header("Settings")

        selected_model_label = st.selectbox(
            "Gemini model",
            options=list(MODEL_OPTIONS.keys()),
            index=list(MODEL_OPTIONS.keys()).index(DEFAULT_MODEL_LABEL),
        )

        api_key_input = st.text_input(
            "Gemini API key",
            type="password",
        )

        st.divider()
        st.markdown("### How to use")

        st.markdown(
            """
        1. Upload a PDF file.
        2. Use **Summary** to generate study notes from the whole document.
        3. Use **Quiz** to choose specific chunks and generate practice questions.
        4. Use **Ask PDF** to ask questions about the document.
        """
        )

        st.markdown("### Technical approach")

        st.markdown(
            f"""
        - **PDF processing:** the document is extracted into text and split into overlapping chunks.
        - **Summary:** uses a map-reduce approach, so every chunk is summarized before the final summary is created.
        - **Quiz:** uses only the chunks selected by the user.
        - **Ask PDF:** uses lightweight RAG with local embeddings to retrieve the {QA_TOP_K} most relevant chunks.
        - **Embedding model:** `{EMBEDDING_MODEL_NAME}`.
        """
        )

    return MODEL_OPTIONS[selected_model_label], get_api_key(api_key_input)


def load_uploaded_pdf(uploaded_pdf) -> tuple[str, int, list[str], float]:
    pdf_status = st.empty()

    try:
        pdf_status.info("Reading text from PDF...")
        pdf_start = time.time()
        pdf_bytes = uploaded_pdf.getvalue()
        reset_outputs_when_pdf_changes(pdf_bytes)
        pdf_text, page_count = read_pdf_text_from_bytes(pdf_bytes)
        pdf_read_time = time.time() - pdf_start
        pdf_status.success("PDF loaded successfully.")
    except Exception as exc:
        pdf_status.error(str(exc))
        st.stop()

    if not pdf_text:
        st.error("Could not extract text from the PDF. It may be a scanned document without a text layer.")
        st.stop()

    chunks = split_text_into_chunks(pdf_text, SUMMARY_CHUNK_CHARS, SUMMARY_CHUNK_OVERLAP)
    return pdf_text, page_count, chunks, pdf_read_time
