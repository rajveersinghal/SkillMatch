import pdfplumber
import docx

def extract_text_from_pdf(file) -> str:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text.strip()


def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs]).strip()


def extract_text(uploaded_file) -> str:
    """
    Extract text from an uploaded file (PDF or DOCX).
    Wrapper function to handle different file types.
    """
    if uploaded_file.type == "application/pdf":
        try:
            return extract_text_from_pdf(uploaded_file)
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            return extract_text_from_docx(uploaded_file)
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    else:
        return ""

