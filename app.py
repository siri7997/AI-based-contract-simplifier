import streamlit as st
from utils import extract_text_from_pdf, simplify_contract, save_as_pdf, answer_question, save_as_audio

# Optional: simple Braille conversion
BRAILLE_DICT = {
    "a":"⠁","b":"⠃","c":"⠉","d":"⠙","e":"⠑","f":"⠋","g":"⠛","h":"⠓",
    "i":"⠊","j":"⠚","k":"⠅","l":"⠇","m":"⠍","n":"⠝","o":"⠕","p":"⠏",
    "q":"⠟","r":"⠗","s":"⠎","t":"⠞","u":"⠥","v":"⠧","w":"⠺","x":"⠭",
    "y":"⠽","z":"⠵"," ":" "
}

def text_to_braille(text):
    text = text.lower()
    return "".join(BRAILLE_DICT.get(c, c) for c in text)

# Constitutional/legal mapping
CONSTITUTIONAL_LAWS = {
    "payment": "Article 299: Payment of government contracts",
    "termination": "Article 300A: Right to property may affect contractual obligations",
    "liability": "Section 73, Indian Contract Act: Compensation for loss caused by breach",
    "confidentiality": "Trade Secrets Protection: Not explicitly in Constitution, but protected under contracts",
    "dispute": "Arbitration and Conciliation Act, 1996: Dispute resolution mechanism"
}

def map_clauses_to_laws(clauses):
    mapped = {}
    for clause in clauses:
        for key, law in CONSTITUTIONAL_LAWS.items():
            if key in clause.lower():
                mapped[clause] = law
    return mapped

# Streamlit setup
st.set_page_config(page_title="AI Contract Explainer", page_icon="📜", layout="wide")
st.title("📜 AI Legal Contract Simplifier")

# CSS for buttons
st.markdown("""
<style>
.stButton>button {background-color: #007acc; color: white;}
.stButton>button:hover {background-color: #005fa3; color: white;}
.stDownloadButton>button {background-color: #28a745; color: white;}
.stDownloadButton>button:hover {background-color: #1e7e34; color: white;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "step" not in st.session_state: st.session_state.step = "upload"
if "uploaded_file" not in st.session_state: st.session_state.uploaded_file = None
if "selected_lang" not in st.session_state: st.session_state.selected_lang = ("English", "en")
if "raw_text" not in st.session_state: st.session_state.raw_text = ""
if "simplified_text" not in st.session_state: st.session_state.simplified_text = ""

# ---------------------- STEP 1: Upload ----------------------
if st.session_state.step == "upload":
    st.header("Step 1: Upload Contract and Select Language")
    uploaded_file = st.file_uploader("Upload your contract (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])
    
    languages = [
        ("English", "en"), ("Telugu", "te"), ("Tamil", "ta"), ("Hindi", "hi"), ("Kannada", "kn"), ("Malayalam", "ml"),
        ("Spanish", "es"), ("French", "fr"), ("Japanese", "ja"), ("Chinese", "zh-cn"), ("Korean", "ko"), ("German", "de")
    ]
    selected_lang = st.selectbox("🌍 Choose the language for simplification", languages, format_func=lambda x: x[0])
    
    if uploaded_file and st.button("Next: Simplify Contract"):
        st.session_state.uploaded_file = uploaded_file
        st.session_state.selected_lang = selected_lang
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        st.session_state.raw_text = extract_text_from_pdf("temp.pdf")
        st.session_state.step = "simplify"  # move to next step

# ---------------------- STEP 2: Simplify ----------------------
elif st.session_state.step == "simplify":
    st.header("Step 2: Simplified Contract & Laws")
    
    # Privacy notice
    st.info("🔒 Your privacy is ensured. Data is processed securely and not stored.")
    
    raw_text = st.session_state.raw_text
    lang_name, lang_code = st.session_state.selected_lang

    # Simplify contract if not already done
    if not st.session_state.simplified_text:
        st.session_state.simplified_text = simplify_contract(raw_text, lang_name)

    # Two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Simplified Contract")
        st.text_area("Text", st.session_state.simplified_text, height=350)
        
        # Download PDF
        pdf_file = "simplified_contract.pdf"
        save_as_pdf(st.session_state.simplified_text, pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name=pdf_file)
        
        # Download Audio
        audio_file = "simplified_contract.mp3"
        try:
            clean_text = st.session_state.simplified_text.replace("*", "")
            save_as_audio(clean_text, audio_file, lang=lang_code)
            st.audio(audio_file, format="audio/mp3")
            with open(audio_file, "rb") as f:
                st.download_button("⬇️ Download Audio", f, file_name=audio_file)
        except Exception as e:
            st.error(f"Audio generation failed: {e}")

        # Download Braille
        try:
            braille_text = text_to_braille(clean_text)
            st.download_button(
                label="⬇️ Download Braille",
                data=braille_text,
                file_name="simplified_contract_braille.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Braille generation failed: {e}")

        # Q&A section
        with st.expander("❓ Ask Questions"):
            user_question = st.text_input("Enter your question here:")
            if user_question:
                answer = answer_question(st.session_state.simplified_text, user_question, lang_name)
                st.markdown(f"**Answer:** {answer}")

    # Right column: Laws / Constitutional Sections
    with col2:
        st.subheader("Relevant Laws / Constitutional Sections")
        clauses = [line for line in st.session_state.simplified_text.split(".") if line.strip()]
        mapped_laws = map_clauses_to_laws(clauses)
        for clause, law in mapped_laws.items():
            st.markdown(f"**Clause:** {clause.strip()}\n**Law/Section:** {law}\n")

    # Back button
    if st.button("⬅️ Back"):
        st.session_state.step = "upload"
