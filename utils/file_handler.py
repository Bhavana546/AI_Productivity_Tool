import PyPDF2
import docx

def load_file(file) -> str:
    if file is None:
        return ""

    filename = file.name.lower()
    try:
        if filename.endswith('.txt'):
            return file.getvalue().decode("utf-8")
        elif filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        elif filename.endswith('.docx'):
            doc = docx.Document(file)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        else:
            return ""
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return ""
