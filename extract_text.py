import pdfplumber
import re
import spacy

nlp = spacy.load('en_core_web_sm')

'''def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text'''

# function to extract text from pdf and save them in a list of strings
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text_lines = []
        for page in pdf.pages:
            text = page.extract_text()
            # Append each line of text as a separate element in a list
            text_lines += text.split('\n')
            
    return text_lines


def preprocess_text_modified(text_lines):
    # Join the list of text lines into a single string
    text = ' '.join(text_lines)
    
    # Remove non-alphanumeric characters and extra whitespaces
    # except characters used in emails, GPAs, "high-fin", and website links
    pattern = r'[^\w\s@.#+-]|(?<=\d)\s+(?=\d)|(?<=high-fin)\W|(?<=[\w\s])[-]'
    
    # Apply the regular expression pattern to the text
    text = re.sub(pattern, ' ', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespaces and line breaks
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Use spaCy to split the preprocessed text into sentences
    doc = nlp(text)
    preprocessed_text_lines = [sent.text for sent in doc.sents]
    return preprocessed_text_lines


'''def preprocess_text(text):
    # Join the list of text lines into a single string
    
    text = ' '.join(text_lines)
    
    # Remove non-alphanumeric characters and extra whitespaces
    # except characters used in emails, GPAs, "high-fin", and website links
    pattern = r'[^\w\s@.#+-]|(?<=\d)\s+(?=\d)|(?<=high-fin)\W|(?<=[\w\s])[-]'
    
    # Apply the regular expression pattern to the text
    text = re.sub(pattern, ' ', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespaces and line breaks
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split the preprocessed text into a list of lines
    text_lines = text.split('\n')
    
    return text_lines'''

'''def preprocess_text(text):
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
    
    return text'''


