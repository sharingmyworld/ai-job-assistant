import pdfplumber


def read_pdf(filename):

    text = ""

    with pdfplumber.open(filename) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text.lower() + "\n"

    return text