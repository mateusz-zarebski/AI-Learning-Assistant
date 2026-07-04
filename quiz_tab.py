import streamlit as st

from config import (
    DEFAULT_QUESTION_COUNT,
    DEFAULT_QUIZ_TEMPERATURE,
    DEFAULT_SELECTED_CHUNKS,
    QUIZ_CHECKBOX_COLUMNS,
)
from display_utils import build_context, show_chunks_debug, show_download_text
from gemini_utils import generate_with_gemini
from prompts import build_quiz_prompt


def calculate_quiz_token_limit(question_count: int) -> int:
    return min(question_count * 1500, 8000)


def get_selected_quiz_chunks(chunks: list[str]) -> tuple[list[str], list[int]]:
    selected_indexes = [index for index in range(len(chunks)) if st.session_state.get(f"quiz_chunk_{index}", False)]
    return [chunks[index] for index in selected_indexes], selected_indexes


def render_quiz_chunk_selector(chunks: list[str]) -> tuple[list[str], list[int], str]:
    st.markdown("### Choose chunks for the quiz")
    st.caption("Select the document chunks that should be used to generate the quiz.")

    left, right = st.columns(2)
    with left:
        if st.button("Select all chunks"):
            for index in range(len(chunks)):
                st.session_state[f"quiz_chunk_{index}"] = True
            st.rerun()
    with right:
        if st.button("Clear selection"):
            for index in range(len(chunks)):
                st.session_state[f"quiz_chunk_{index}"] = False
            st.rerun()

    checkbox_columns = st.columns(QUIZ_CHECKBOX_COLUMNS)
    for index, chunk in enumerate(chunks):
        key = f"quiz_chunk_{index}"
        st.session_state.setdefault(key, index < min(DEFAULT_SELECTED_CHUNKS, len(chunks)))

        with checkbox_columns[index % QUIZ_CHECKBOX_COLUMNS]:
            st.checkbox(f"Chunk {index + 1}", key=key)

    selected_chunks, selected_indexes = get_selected_quiz_chunks(chunks)
    selected_context = build_context(selected_chunks, selected_indexes, len(chunks)) if selected_chunks else ""

    st.info(f"Selected chunks: {len(selected_chunks)} / {len(chunks)}")

    if selected_chunks:
        show_chunks_debug(
            title="Preview selected quiz chunks",
            caption="These fragments will be used for quiz generation.",
            chunks_to_show=selected_chunks,
            chunk_indexes=selected_indexes,
            total_chunks=len(chunks),
            key_prefix="quiz_selected_fragment",
        )
    else:
        with st.expander("Preview selected quiz chunks"):
            st.warning("No chunks selected.")

    return selected_chunks, selected_indexes, selected_context


def render_saved_quiz(model_name: str) -> None:
    if not st.session_state.quiz_result:
        return

    st.success(f"Quiz generated in {st.session_state.quiz_generation_time:.2f} s using {model_name}.")
    st.markdown(st.session_state.quiz_result.replace("\n", "  \n"))
    show_download_text("Download quiz as TXT", st.session_state.quiz_result, "quiz.txt")


def render_quiz_tab(client, model_name: str, chunks: list[str], api_key: str | None) -> None:
    st.subheader("Generate quiz")

    question_count = st.slider("Number of quiz questions", 1, 10, DEFAULT_QUESTION_COUNT, 1)
    quiz_temperature = st.slider(
        "Creativity level",
        min_value=0.0,
        max_value=0.8,
        value=DEFAULT_QUIZ_TEMPERATURE,
        step=0.1,
        help="Lower = more stable. Higher = more varied.",
    )

    selected_chunks, _, selected_context = render_quiz_chunk_selector(chunks)

    if st.button("Generate quiz", type="primary"):
        if not api_key:
            st.error("Missing Gemini API key. Add it in the sidebar, Streamlit secrets, or GEMINI_API_KEY environment variable.")
            st.stop()
        if not selected_chunks:
            st.error("Select at least one chunk before generating a quiz.")
            st.stop()

        try:
            with st.spinner("Generating quiz with Gemini..."):
                quiz, generation_time = generate_with_gemini(
                    client=client,
                    model_name=model_name,
                    prompt=build_quiz_prompt(selected_context, question_count),
                    temperature=quiz_temperature,
                    max_output_tokens=calculate_quiz_token_limit(question_count),
                )

            st.session_state.quiz_result = quiz
            st.session_state.quiz_generation_time = generation_time
        except Exception as exc:
            st.error(str(exc))

    render_saved_quiz(model_name)
