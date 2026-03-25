import zipfile
from pathlib import Path
from pypdf import PdfWriter, PdfReader
from app.config import OUT_DIR

def split_pdf(src: str) -> str:
    reader = PdfReader(src)
    src_path = Path(src)
    
    zip_path = OUT_DIR / f"split_{src_path.stem}.zip"
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            page_name = f"page_{i+1}.pdf"
            temp_path = OUT_DIR / page_name
            
            with open(temp_path, "wb") as f:
                writer.write(f)
            
            zipf.write(temp_path, arcname=page_name)
            temp_path.unlink() # Clean up individual page
            
    return str(zip_path)