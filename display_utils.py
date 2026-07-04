import streamlit as st

from config import PREVIEW_CHARS


def build_context(selected_chunks: list[str], selected_indexes: list[int], total_chunks: int) -> str:
    return "\n\n---\n\n".join(
        f"Fragment {position}/{len(selected_chunks)} "
        f"(chunk {chunk_index + 1}/{total_chunks}):\n{chunk}"
        for position, (chunk, chunk_index) in enumerate(zip(selected_chunks, selected_indexes), start=1)
    )


def show_download_text(label: str, content: str, file_name: str) -> None:
    st.download_button(label=label, data=content, file_name=file_name, mime="text/plain")


def show_chunks_debug(title: str, caption: str, chunks_to_show: list[str], chunk_indexes: list[int], total_chunks: int, key_prefix: str, scores: list[float] | None = None,) -> None:
    with st.expander(title):
        st.caption(caption)

        for position, (chunk, chunk_index) in enumerate(zip(chunks_to_show, chunk_indexes), start=1):
            score_text = "" if scores is None else f" — similarity: {scores[position - 1]:.3f}"
            st.markdown(
                f"**Chunk {position}/{len(chunks_to_show)} — "
                f"source chunk {chunk_index + 1}/{total_chunks}{score_text}**"
            )
            st.text_area(
                label=f"{key_prefix} chunk {chunk_index + 1}",
                value=chunk,
                height=180,
                disabled=True,
                key=f"{key_prefix}_{chunk_index}_{position}",
            )


def show_pdf_info(pdf_text: str, page_count: int, chunk_count: int, read_time: float) -> None:
    left, right = st.columns([2, 1])

    with left:
        st.subheader("PDF text preview")

        preview = pdf_text[:PREVIEW_CHARS]
        if len(pdf_text) > PREVIEW_CHARS:
            preview += "..."

        st.text_area(
            "Extracted text preview",
            value=preview,
            height=360,
            disabled=True,
        )

    with right:
        st.subheader("PDF information")
        st.metric("Pages", page_count)
        st.metric("Chunks", chunk_count)
        st.metric("Characters", f"{len(pdf_text):,}".replace(",", " "))
        st.metric("Reading time", f"{read_time:.2f} s")
