MODEL_OPTIONS = {
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 2.5 Flash-Lite": "gemini-2.5-flash-lite",
}

DEFAULT_MODEL_LABEL = "Gemini 2.5 Flash"
PREVIEW_CHARS = 10000

SUMMARY_CHUNK_CHARS = 3000
SUMMARY_CHUNK_OVERLAP = 300
SUMMARY_TEMPERATURE = 0.2

DEFAULT_SELECTED_CHUNKS = 3
DEFAULT_QUESTION_COUNT = 3
DEFAULT_QUIZ_TEMPERATURE = 0.2
QUIZ_CHECKBOX_COLUMNS = 5

QA_TEMPERATURE = 0.1
QA_TOP_K = 4
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

OUTPUT_STATE_DEFAULTS = {
    "summary_result": None,
    "summary_generation_time": None,
    "summary_partial_summaries": None,
    "quiz_result": None,
    "quiz_generation_time": None,
    "qa_answer": None,
    "qa_generation_time": None,
    "qa_retrieval_time": None,
    "qa_retrieved_chunks": None,
    "qa_retrieved_indexes": None,
    "qa_similarity_scores": None,
}
