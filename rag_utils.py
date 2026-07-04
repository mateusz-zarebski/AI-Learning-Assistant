import numpy as np
import streamlit as st

from config import EMBEDDING_MODEL_NAME, QA_TOP_K

@st.cache_resource(show_spinner=False)
def load_embedding_model(model_name: str):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError("Missing sentence-transformers. Install it with: pip install sentence-transformers") from exc

    return SentenceTransformer(model_name)

@st.cache_data(show_spinner=False)
def create_chunk_embeddings(chunks_tuple: tuple[str, ...], model_name: str) -> np.ndarray:
    model = load_embedding_model(model_name)
    embeddings = model.encode(list(chunks_tuple), normalize_embeddings=True, show_progress_bar=False)
    return np.asarray(embeddings, dtype=np.float32)


def select_relevant_chunks_with_rag(chunks: list[str], question: str, top_k: int = QA_TOP_K, model_name: str = EMBEDDING_MODEL_NAME,) -> tuple[list[str], list[int], list[float]]:
    question = question.strip()
    if not chunks or not question:
        return [], [], []

    model = load_embedding_model(model_name)
    chunk_embeddings = create_chunk_embeddings(tuple(chunks), model_name)
    question_embedding = model.encode([question], normalize_embeddings=True, show_progress_bar=False)
    question_embedding = np.asarray(question_embedding, dtype=np.float32)[0]

    scores = chunk_embeddings @ question_embedding
    top_indexes = np.argsort(scores)[::-1][: min(top_k, len(chunks))].tolist()

    return (
        [chunks[index] for index in top_indexes],
        top_indexes,
        [float(scores[index]) for index in top_indexes],
    )
