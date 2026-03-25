import os
from pypdf import PdfReader, PdfWriter
from app.config import OUT_DIR
from app.util.help import out_path

def compress_pdf(input_path: str) -> str:
    """
    Compresses a PDF by reducing its content streams.
    """
    output_file = out_path(input_path, ".pdf")
    
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            # Correctly add the page to the writer object
            writer.add_page(page)

        # Apply compression to all pages now that they are part of the writer
        for page in writer.pages:
            page.compress_content_streams()  # This reduces file size

        with open(output_file, "wb") as f:
            writer.write(f)

        return output_file
    except Exception as e:
        # Fallback if compression fails
        if os.path.exists(output_file):
            os.remove(output_file)
        raise Exception(f"Compression failed: {str(e)}")