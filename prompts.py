def build_chunk_summary_prompt(chunk_text: str, chunk_number: int, total_chunks: int) -> str:
    return f"""
You are an AI study-notes extractor.

Extract useful study notes from this PDF fragment.

Your task:
- Preserve the most important learning content from this fragment.
- Capture key definitions, facts, processes, comparisons and relationships.
- Keep the notes useful for a student.
- Do not create a very short abstract.
- Do not create exhaustive textbook notes.

Critical rules:
- Use only information from this PDF fragment.
- Do not add outside knowledge.
- Do not guess missing information.
- If a sentence is cut off, ignore the incomplete part.
- Write only in English.
- Be detailed enough to study from, but concise.
- Prefer concrete facts over general statements.
- Preserve the order of topics as they appear in the fragment.
- Prioritize the most important information.
- Do not try to include every small detail.
- Write 8-14 bullet points maximum in Detailed study notes.
- Write only the most important terms, processes and comparisons.
- Do not include an introduction.
- Do not include a conclusion.
- Make sure the answer does not end with an unfinished sentence.

Required format:

Fragment {chunk_number}/{total_chunks}

Topics covered:
- [topic]
- [topic]
- [include only the main topics]

Detailed study notes:
- [important fact, definition, process, comparison or relationship]
- [important fact, definition, process, comparison or relationship]
- [8-14 bullets maximum]

Important terms, processes and comparisons:
- [term/process/comparison]&#58; [short explanation]
- [term/process/comparison]&#58; [short explanation]
- [include only the most important items]

High-yield facts:
- [fact useful for revision or quiz]
- [fact useful for revision or quiz]
- [3-6 facts maximum]

Before finalizing, check that:
- the notes are useful but not exhaustive,
- the most important information from the fragment is represented,
- definitions, processes and comparisons are included if important,
- no outside information was added,
- the answer does not end with an unfinished sentence.

PDF FRAGMENT:
{chunk_text}
""".strip()


def build_final_summary_prompt(partial_summaries: str) -> str:
    return f"""
You are an AI learning assistant.

Create a clear medium-length study summary of the whole document based only on the partial summaries below.

Your task:
- Explain what the document is about.
- Describe the main topics in the order they appear.
- Extract the most important learning points.
- Organize the material so a student can revise from it.
- Preserve key definitions, processes, comparisons and facts.

Critical rules:
- Use only information from the partial summaries.
- Do not add outside knowledge.
- Do not guess missing information.
- Do not mention cut off or missing source text.
- Do not only list topic names.
- Write only in English.
- Be clear, structured and useful for studying.
- Keep the order of the document in the topic walkthrough.
- Keep the final summary medium-length, not exhaustive.
- Do not turn the summary into full textbook notes.
- If many topics are present, summarize each topic briefly instead of expanding every detail.
- Use 2-4 bullets maximum per topic section.
- Include only the most important definitions, processes and comparisons.
- Do not include every small detail from the partial summaries.
- Make sure the answer does not end with an unfinished sentence.
- At the very end of the summary, write exactly: END OF SUMMARY

Required format:

# Study Summary

## What this document is about
[Write 4-6 sentences explaining the overall subject and learning purpose of the document.]

## Topic walkthrough
- [Describe the first main topic and its key ideas.]
- [Describe the next main topic and its key ideas.]
- [Continue briefly through the document in order.]
- [Do not expand every detail here.]

## Main study notes

### [Topic name]
- [important fact, definition, relationship, process or comparison]
- [important fact, definition, relationship, process or comparison]
- [2-4 bullets maximum for this topic]

### [Topic name]
- [important fact, definition, relationship, process or comparison]
- [important fact, definition, relationship, process or comparison]
- [2-4 bullets maximum for this topic]

[Add more topic sections only for major topics.]

## Key definitions
- [term]&#58; [definition]
- [term]&#58; [definition]
- [include only the most important definitions]

## Important processes and comparisons
- [process or comparison]&#58; [short explanation]
- [process or comparison]&#58; [short explanation]
- [include only the most important items]

## High-yield facts for revision
- [important fact]
- [important fact]
- [important fact]
- [5-10 facts maximum]

END OF SUMMARY

Before finalizing, check that:
- the summary follows the document order,
- the summary is medium-length, not exhaustive,
- the main study notes contain concrete facts,
- only the most important definitions, processes and comparisons are included,
- no outside information was added,
- the answer does not end with an unfinished sentence,
- the final line is exactly: END OF SUMMARY.

PARTIAL SUMMARIES:
{partial_summaries}
""".strip()


def build_quiz_prompt(context_text: str, question_count: int) -> str:
    return f"""
You are an AI quiz generator.

Generate exactly {question_count} complete multiple-choice quiz questions based only on the PDF fragments below.

Critical rules:
- You must generate exactly {question_count} questions.
- Do not generate fewer than {question_count} questions.
- Do not stop after the first question.
- Use only information from the PDF fragments.
- Do not add outside knowledge.
- Each question must test understanding, not simple copying.
- Each question must focus on one clear idea.
- Each question must have exactly 4 answer options: A, B, C, D.
- Exactly one answer must be correct.
- Wrong answers should be realistic but clearly incorrect.
- Do not include explanations.
- Do not include an introduction.
- Do not include a conclusion.
- Write only in English.
- At the very end of the quiz, write exactly: END OF QUIZ

Required format for each question:

[number]. [question text]
A) [answer]
B) [answer]
C) [answer]
D) [answer]
Correct answer: [A/B/C/D]

Repeat this format until you have exactly {question_count} questions.

END OF QUIZ

Before finalizing, check that:
- there are exactly {question_count} numbered questions,
- questions are numbered from 1 to {question_count},
- each question has A, B, C and D,
- each question has exactly one "Correct answer:",
- exactly one answer is correct for each question,
- there are no explanations,
- the final line is exactly: END OF QUIZ.

PDF FRAGMENTS:
{context_text}
""".strip()


def build_question_prompt(context_text: str, user_question: str) -> str:
    return f"""
You are an AI learning assistant.

Answer the student's question using only facts supported by the retrieved PDF fragments.
Do not merely copy sentences from the PDF. Explain the meaning in your own words.

Your job:
- Give a direct answer.
- Explain the concept simply, like to a student.
- Use the retrieved PDF fragments as evidence.
- You may rephrase and clarify information from the PDF.
- You may connect facts from different provided fragments if they are clearly related.
- Do not add new facts that are not supported by the fragments.
- Analogies are allowed only if they clearly explain facts from the PDF and do not introduce new claims.
- If the fragments do not contain enough information, say that clearly.

Answer format:

Direct answer:
[1-2 sentences answering the question directly]

Simple explanation:
[2-5 sentences explaining what it means in easier words]

Evidence from the PDF:
[briefly state which sentence or idea from the PDF supports the answer, with page number if available]

User question:
{user_question}

RETRIEVED PDF FRAGMENTS:
{context_text}
""".strip()
