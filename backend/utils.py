# backend/utils.py
import re
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    """Extracts text content from a PDF file."""
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def clean_text(text):
    """Cleans the text by removing extra whitespace and special characters."""
    if text:
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return ""