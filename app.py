from googletrans import Translator
import streamlit as st

st.title("Translator (Test Version)")

text = st.text_area("Enter text to translate:")
target_lang = st.text_input("Target language code (e.g., sw for Swahili, fr for French):")

if st.button("Translate"):
    if text and target_lang:
        translator = Translator()
        result = translator.translate(text, dest=target_lang)
        st.success(f"Translation: {result.text}")
    else:
        st.error("Please enter text and target language.")
