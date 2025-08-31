from groq import Groq
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from gtts import gTTS
import os

# ✅ API key (⚠️ load from env in production)
client = Groq(api_key="API_KEY")

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def simplify_contract(text, target_language="english"):
    """Simplify and translate contract into target language"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": f"You are a multilingual legal assistant. Detect the input language. Simplify it into plain terms. Then translate into {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content

def answer_question(contract_text, question, target_language="english"):
    """Answer user's questions about the contract in their chosen language"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": f"You are a helpful multilingual legal assistant. Answer questions clearly in {target_language}."},
            {"role": "user", "content": f"Contract:\n{contract_text}\n\nQuestion: {question}"},
        ],
    )
    return response.choices[0].message.content

def save_as_pdf(text, output_path="simplified_contract.pdf"):
    """Save text as a new PDF"""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    y = height - 40
    for line in text.split("\n"):
        c.drawString(40, y, line[:100])  # truncate long lines
        y -= 15
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()

def save_as_audio(text, output_path="simplified_contract.mp3", lang="en"):
    """
    Convert text into speech and save as MP3.
    Supported language codes: en, hi, te, ta, kn, ml, es, fr, de, ja, zh-cn, ko, etc.
    """
    if not text or not text.strip():
        raise ValueError("No text provided for audio generation.")

    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)
    return output_path
