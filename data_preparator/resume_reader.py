import pdfplumber
class ResumeReader:

    file_path: str
    extracted_text: str

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.extracted_text = ""

    def extract_text(self) -> str:
        if self.file_path.endswith(".pdf"):
            self.read_pdf_resume()
            if self.extracted_text == "":
                raise "No text extracted"
            return self.extracted_text

    def read_pdf_resume(self):
        try:
            with pdfplumber.open(self.file_path) as pdf:
                pages = pdf.pages
                for page in pages:
                    self.extracted_text += page.extract_text()
            return self.extracted_text
        except Exception as e:
            print(f"Error occurred while reading a file: {e}")
            raise "Error occurred while reading a file"


if __name__ == "__main__":
    reader = ResumeReader("../resources/resume/ML_Engineer_Nurmukhammed_Urazbaev.pdf")
    reader.extract_text()
    print(reader.extracted_text)
