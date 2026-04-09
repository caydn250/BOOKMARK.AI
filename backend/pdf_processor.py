"""
PDF text extraction and processing module
"""
import pdfplumber
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n[Page {page_num}]\n{page_text}"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        raise
    
    return text


def extract_sentences(text):
    """
    Split text into sentences for processing.
    
    Args:
        text: Raw text from PDF
        
    Returns:
        list: List of sentences
    """
    import nltk
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    sentences = nltk.sent_tokenize(text)
    # Filter out very short sentences and page markers
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    return sentences


def clean_text(text):
    """
    Clean and normalize text.
    
    Args:
        text: Raw text
        
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text
