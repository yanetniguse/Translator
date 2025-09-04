from flask import Flask, render_template, request, send_file
from google.cloud import translate
import os
import pdfplumber
from docx import Document
import io

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/YanetNiguse/Desktop/En_to_AfricanLan/credentials.json"

app = Flask(__name__)

# Initialize Google Translate client
translate_client = translate.TranslationServiceClient()

def extract_text(file):
    ext = file.filename.split('.')[-1].lower()
    text = ""
    if ext == 'txt':
        text = file.read().decode('utf-8')
    elif ext == 'pdf':
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    elif ext == 'docx':
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def translate_text(text, target_lang):
    project_id = "your-project-id"  # replace with your GCP project ID
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


@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""
    if request.method == 'POST':
        file = request.files['file']
        target_lang = request.form['language']
        text = extract_text(file)
        translated_text = translate_text(text, target_lang)
    return render_template('index.html', translated_text=translated_text)

if __name__ == '__main__':
    # Make sure to set GOOGLE_APPLICATION_CREDENTIALS env variable for API key
    app.run(debug=True)
