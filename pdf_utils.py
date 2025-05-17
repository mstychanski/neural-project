
import os
import fitz

def extract_pdf_info(uploaded_file):
    if getattr(uploaded_file, "size", None) == 0:
        return {
            "filename": uploaded_file.name,
            "text": ""
        }
    try:
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        num_pages = pdf_doc.page_count
        if num_pages > 0:
            first_page = pdf_doc.load_page(0)
            text = first_page.get_text() or ""
        else:
            text = ""
    except Exception:
        text = ""
    return {
        "filename": uploaded_file.name,
        "text": text
    }


def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def load_documents_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            text = load_pdf(os.path.join(folder_path, filename))
            documents.append({"filename": filename, "text": text})
    return documents