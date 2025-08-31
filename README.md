# AI-based-contract-simplifier
Legal contracts are often complex and difficult for non-experts to understand, leading to misinterpretations. Build a Gen AI tool that takes complex legal contracts as input and generates simplified, layperson-friendly summaries or explanations while preserving key terms and obligations. 
so i created :
A Streamlit-based web application that allows users to upload legal contracts and automatically simplify them into plain language, with features like translation, audio output, Braille export, and relevant legal clause mapping.

Project Structure
app.py – Main Streamlit application. Handles:

File upload (PDF/Image contracts)

Contract simplification and translation

Display of simplified text

Download options (PDF, Audio, Braille)

Q&A on contract content

Mapping contract clauses to relevant laws/constitutional sections

utils.py – Backend utilities. Handles:

PDF text extraction (extract_text_from_pdf)

Contract simplification via LLM (simplify_contract)

Question answering (answer_question)

PDF export (save_as_pdf)

Text-to-speech audio generation (save_as_audio)

Features
Contract Upload – Accepts PDFs or images.

Multilingual Simplification – Supports English, Hindi, Tamil, Telugu, Spanish, French, German, Japanese, Chinese, Korean, etc.

Audio Output – Converts simplified contract into MP3 using gTTS.

Braille Output – Optional text-to-Braille conversion for accessibility.

Clause-to-Law Mapping – Maps keywords in contract to predefined legal references.

Interactive Q&A – Users can ask questions about the simplified contract and get answers.

How It Works
User uploads a contract and selects a language.

utils.extract_text_from_pdf() extracts the raw text.

utils.simplify_contract() sends the text to a large language model (LLM) to simplify and translate it.

Simplified text is displayed in the app, along with:

Downloadable PDF (utils.save_as_pdf)

Audio MP3 (utils.save_as_audio)

Braille text (optional)

Clauses in the contract are mapped to relevant laws using map_clauses_to_laws().

Requirements
Python 3.10+

Streamlit

PyPDF2

reportlab

gTTS

Groq API client (for LLM)
