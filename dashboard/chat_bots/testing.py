import PyPDF2

pdf_path = 'F:\\WORKspace\\RAGOPS v2\\media\\uploaded_files\\Devs_Resume.pdf'
def pdf_to_text(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            num_pages = pdf_reader.numPages

            for page_number in range(num_pages):
                page = pdf_reader.getPage(page_number)
                text += page.extractText()

        return text
    except Exception as e:
        print(f"Error processing PDF '{pdf_path}': {e}")
        return None

class PDFProcessor:
    def __init__(self, pdf_paths):
        self.pdf_paths = pdf_paths

    def process_pdfs(self):
        combined_text = ""
        for pdf_path in self.pdf_paths:
            text = pdf_to_text(pdf_path)
            combined_text += text
        return combined_text