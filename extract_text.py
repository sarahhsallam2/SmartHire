import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def preprocess_text(text):
    # Remove non-alphanumeric characters and extra whitespaces
    # except characters used in emails, GPAs, "high-fin", and website links
    pattern = r'[^\w\s@.#+-]|(?<=\d)\s+(?=\d)|(?<=high-fin)\W|(?<=[\w\s])[-]'
    
    # Apply the regular expression pattern to the text
    text = re.sub(pattern, ' ', text)
    #text = re.sub(r'\W+', ' ', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespaces and line breaks
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


