import streamlit as st
from google.cloud import translate
import os
import pdfplumber
from docx import Document
import io

# ⚡ Set Google Credentials (make sure you upload credentials.json to Streamlit secrets instead of hardcoding path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Initialize Google Translate client
translate_client = translate.TranslationServiceClient()

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
    project_id = "your-project-id"  # Replace with your actual GCP project ID
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en",
            "target_language_code": target_lang,
        }
    )

    return response.translations[0].translated_text

# ---------------- Streamlit UI ---------------- #
st.title("🌍 English → African Languages Translator")

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
