import streamlit as st
from google.cloud import translate
from google.oauth2 import service_account
import pdfplumber
from docx import Document

# Load credentials from Streamlit secrets
creds = service_account.Credentials.from_service_account_info(
    st.secrets["google_cloud"]
)

# Initialize client with credentials
translate_client = translate.TranslationServiceClient(credentials=creds)

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
    project_id = st.secrets["google_cloud"]["project_id"]
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
