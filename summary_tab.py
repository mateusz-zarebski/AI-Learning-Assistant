import time

import streamlit as st

from config import SUMMARY_TEMPERATURE
from display_utils import show_download_text
from gemini_utils import generate_with_gemini
from prompts import build_chunk_summary_prompt, build_final_summary_prompt


def generate_map_reduce_summary(
    client,
    model_name: str,
    chunks: list[str],
    temperature: float,
) -> tuple[str, float, list[str]]:
    if not chunks:
        raise ValueError("No chunks available for summarization.")

    total_start = time.time()
    partial_summaries = []
    progress_bar = st.progress(0)
    status = st.empty()

    for index, chunk in enumerate(chunks, start=1):
        status.info(f"Summarizing fragment {index}/{len(chunks)}...")
        prompt = build_chunk_summary_prompt(chunk_text=chunk, chunk_number=index, total_chunks=len(chunks))
        partial_summary, _ = generate_with_gemini(
            client=client,
            model_name=model_name,
            prompt=prompt,
            temperature=0.1,
            max_output_tokens=3000,
        )
        partial_summaries.append(partial_summary)
        progress_bar.progress(index / (len(chunks) + 1))

    status.info("Creating final summary from partial summaries...")
    final_summary, _ = generate_with_gemini(
        client=client,
        model_name=model_name,
        prompt=build_final_summary_prompt("\n\n---\n\n".join(partial_summaries)),
        temperature=temperature,
        max_output_tokens=5000,
    )

    progress_bar.progress(1.0)
    status.success("Map-reduce summary generated.")
    return final_summary, time.time() - total_start, partial_summaries


def render_saved_summary(model_name: str) -> None:
    if not st.session_state.summary_result:
        return

    partials = st.session_state.summary_partial_summaries or []
    st.success(
        f"Full summary generated in {st.session_state.summary_generation_time:.2f} s using {model_name}. "
        f"Gemini calls: {len(partials) + 1}."
    )
    st.markdown(st.session_state.summary_result)

    with st.expander("Debug: partial chunk summaries used to create the final summary"):
        st.caption("These intermediate summaries were used internally to create the final summary.")
        for index, partial_summary in enumerate(partials, start=1):
            st.markdown(f"### Partial summary {index}/{len(partials)}")
            st.markdown(partial_summary)

    show_download_text("Download summary as TXT", st.session_state.summary_result, "summary.txt")


def render_summary_tab(client, model_name: str, chunks: list[str], api_key: str | None) -> None:
    st.subheader("Generate full summary")

    if len(chunks) > 20:
        st.warning(
            f"This PDF has {len(chunks)} chunks. Full map-reduce will make "
            f"{len(chunks) + 1} Gemini calls. For very large PDFs, this may use more API quota."
        )

    if st.button("Generate full summary", type="primary"):
        if not api_key:
            st.error("Missing Gemini API key. Add it in the sidebar, Streamlit secrets, or GEMINI_API_KEY environment variable.")
            st.stop()

        try:
            with st.spinner("Generating map-reduce summary with Gemini..."):
                summary, generation_time, partial_summaries = generate_map_reduce_summary(
                    client=client,
                    model_name=model_name,
                    chunks=chunks,
                    temperature=SUMMARY_TEMPERATURE,
                )

            st.session_state.summary_result = summary
            st.session_state.summary_generation_time = generation_time
            st.session_state.summary_partial_summaries = partial_summaries
        except Exception as exc:
            st.error(str(exc))

    render_saved_summary(model_name)
