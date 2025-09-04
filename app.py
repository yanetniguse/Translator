import streamlit as st
from googletrans import Translator
import pdfplumber
from docx import Document
import io

# Initialize translator
translator = Translator()

def extract_text(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()
    text = ""
    if ext == 'txt':
        text = uploaded_file.read().decode('utf-8')
    elif ext == 'pdf':
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    elif ext == 'docx':
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def translate_text(text, target_lang):
    result = translator.translate(text, dest=target_lang)
    return result.text

# ---------------- Streamlit UI ---------------- #
st.title("🌍 English → African Languages Translator (Free Testing)")

uploaded_file = st.file_uploader("Upload a file (TXT, PDF, DOCX)", type=["txt", "pdf", "docx"])
target_lang = st.text_input("Enter target language code (e.g., 'sw' for Swahili, 'am' for Amharic)")

if uploaded_file and target_lang:
    if st.button("Translate"):
        with st.spinner("Translating..."):
            text = extract_text(uploaded_file)
            if text.strip():
                translated_text = translate_text(text, target_lang)
                st.subheader("✅ Translated Text")
                st.write(translated_text)
            else:
                st.warning("No text could be extracted from the file.")
