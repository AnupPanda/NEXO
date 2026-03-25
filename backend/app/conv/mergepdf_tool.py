import uuid
from pypdf import PdfWriter
from app.config import OUT_DIR

def merge_pdfs(paths: list) -> str:
    merger = PdfWriter()
    try:
        for pdf in paths:
            merger.append(pdf)
        
        out_path = OUT_DIR / f"merged_{uuid.uuid4().hex[:8]}.pdf"
        with open(out_path, "wb") as f:
            merger.write(f)
        merger.close()
        return str(out_path)
    except Exception as e:
        raise Exception(f"PDF Merge failed: {str(e)}")