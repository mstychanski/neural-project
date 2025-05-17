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
