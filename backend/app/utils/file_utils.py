from io import BytesIO
from typing import Union
from pypdf import PdfReader


def extract_text_from_pdf(file_input: Union[BytesIO, bytes]) -> str:
    """
    Extracts text content from a PDF file.
    Accepts either a bytes object or a BytesIO stream.
    """
    try:
        # If the input is raw bytes, wrap it in a BytesIO stream
        if isinstance(file_input, bytes):
            file_stream = BytesIO(file_input)
        else:
            file_stream = file_input

        # Ensure the stream is at the beginning
        file_stream.seek(0)

        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error while extracting text from pdf: {e}")
        raise e
