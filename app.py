import streamlit as st

from display_utils import show_pdf_info
from gemini_utils import get_gemini_client
from qa_tab import render_question_tab
from quiz_tab import render_quiz_tab
from summary_tab import render_summary_tab
from ui import init_output_state, load_uploaded_pdf, render_sidebar


st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="📚",
    layout="wide",
)


def main() -> None:
    init_output_state()

    st.title("📚 AI Learning Assistant")
    st.write(
        "Upload a PDF, then generate a study summary, quiz, or ask questions about the document."
    )

    model_name, api_key = render_sidebar()
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_pdf is None:
        st.info("Upload a PDF file to start.")
        st.stop()

    pdf_text, page_count, chunks, pdf_read_time = load_uploaded_pdf(uploaded_pdf)
    show_pdf_info(pdf_text, page_count, len(chunks), pdf_read_time)

    client = get_gemini_client(api_key) if api_key else None
    summary_tab, quiz_tab, question_tab = st.tabs(["Summary", "Quiz", "Ask PDF"])

    with summary_tab:
        render_summary_tab(client, model_name, chunks, api_key)

    with quiz_tab:
        render_quiz_tab(client, model_name, chunks, api_key)

    with question_tab:
        render_question_tab(client, model_name, chunks, api_key)


if __name__ == "__main__":
    main()
