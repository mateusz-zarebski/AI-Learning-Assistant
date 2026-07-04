import time

import streamlit as st

from config import EMBEDDING_MODEL_NAME, QA_TEMPERATURE, QA_TOP_K
from display_utils import build_context, show_chunks_debug
from gemini_utils import generate_with_gemini
from prompts import build_question_prompt
from rag_utils import select_relevant_chunks_with_rag


def render_saved_qa(model_name: str, total_chunks: int) -> None:
    if not st.session_state.qa_answer:
        return

    st.success(
        f"Answer generated in {st.session_state.qa_generation_time:.2f} s using {model_name}. "
        f"Retrieval time: {st.session_state.qa_retrieval_time:.2f} s."
    )
    st.markdown(st.session_state.qa_answer)

    show_chunks_debug(
        title="Debug: retrieved chunks for this answer",
        caption="These chunks were selected by semantic similarity between the question and the PDF chunks.",
        chunks_to_show=st.session_state.qa_retrieved_chunks or [],
        chunk_indexes=st.session_state.qa_retrieved_indexes or [],
        total_chunks=total_chunks,
        key_prefix="qa_rag_fragment_saved",
        scores=st.session_state.qa_similarity_scores or [],
    )


def render_question_tab(client, model_name: str, chunks: list[str], api_key: str | None) -> None:
    st.subheader("Ask a question about the PDF")
 
    user_question = st.text_input("Your question", placeholder="Example: What is negative feedback in homeostasis?")

    if st.button("Ask PDF", type="primary"):
        if not api_key:
            st.error("Missing Gemini API key. Add it in the sidebar, Streamlit secrets, or GEMINI_API_KEY environment variable.")
            st.stop()
        if not user_question.strip():
            st.error("Write a question first.")
            st.stop()

        try:
            retrieval_start = time.time()
            with st.spinner("Retrieving relevant chunks with local embeddings..."):
                relevant_chunks, relevant_indexes, similarity_scores = select_relevant_chunks_with_rag(
                    chunks=chunks,
                    question=user_question,
                    top_k=QA_TOP_K,
                    model_name=EMBEDDING_MODEL_NAME,
                )
            retrieval_time = time.time() - retrieval_start

            if not relevant_chunks:
                st.error("No relevant chunks found.")
                st.stop()

            question_context = build_context(relevant_chunks, relevant_indexes, len(chunks))

            with st.spinner("Generating answer with Gemini..."):
                answer, generation_time = generate_with_gemini(
                    client=client,
                    model_name=model_name,
                    prompt=build_question_prompt(question_context, user_question),
                    temperature=QA_TEMPERATURE,
                    max_output_tokens=1800,
                )

            st.session_state.qa_answer = answer
            st.session_state.qa_generation_time = generation_time
            st.session_state.qa_retrieval_time = retrieval_time
            st.session_state.qa_retrieved_chunks = relevant_chunks
            st.session_state.qa_retrieved_indexes = relevant_indexes
            st.session_state.qa_similarity_scores = similarity_scores
        except Exception as exc:
            st.error(str(exc))

    render_saved_qa(model_name, len(chunks))
