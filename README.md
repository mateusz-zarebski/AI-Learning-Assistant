# AI Learning Assistant 📚

Streamlit web application that helps students learn from PDF documents.
The app allows users to upload a PDF, generate structured study summaries,
create multiple-choice quizzes from selected document chunks,
and ask questions about the document using lightweight retrieval-augmented generation.

## Features

- PDF upload and text extraction
- Text cleaning and overlapping chunk generation
- Full document study summary using a map-reduce approach
- Quiz generation from user-selected document chunks
- Question answering over the uploaded PDF
- Lightweight RAG using local sentence-transformer embeddings
- Retrieved chunk debug view for transparency
- TXT export for generated summaries and quizzes

## Screenshots

### PDF upload and text preview

![PDF upload and text preview](assets/pdf-preview.png)

### Study summary generation

![Study summary generation](assets/study-summary.png)

### Quiz generator

![Quiz generator](assets/quiz-generator.png)

### Ask PDF

![Ask PDF](assets/ask-pdf-answer.png)

## How It Works

1. The user uploads a PDF document.
2. The app extracts text from the PDF using `pypdf`.
3. The extracted text is cleaned and split into overlapping chunks.
4. For summarization, each chunk is summarized separately, then Gemini creates a final study summary from the partial summaries.
5. For quiz generation, the user selects specific chunks and Gemini creates multiple-choice questions based only on those fragments.
6. For Q&A, local embeddings are created for document chunks. The most relevant chunks are retrieved using semantic similarity and passed to Gemini together with the user question.




## Technologies
- Python
- Streamlit
- Google Gemini API
- pypdf
- sentence-transformers
- NumPy





## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

---
⭐ **Star if you like the project!**  

**Author:** Mateusz Zarebski  
[GitHub Profile](https://github.com/mateusz-zarebski) | [Portfolio Overview](https://github.com/mateusz-zarebski/portfolio)













