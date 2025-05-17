import fitz

def extract_pdf_info(uploaded_file):
    pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    num_pages = pdf_doc.page_count
    if num_pages > 0:
        first_page = pdf_doc.load_page(0)
        text = first_page.get_text()
    else:
        text = "Brak stron w pliku."
    return {
        "name": uploaded_file.name,
        "num_pages": num_pages,
        "text": text
    }
