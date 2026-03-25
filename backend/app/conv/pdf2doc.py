from pathlib import Path
from pdf2docx import Converter
from app.config import OUT_DIR


def convert_pdf_to_docx(src: str) -> str:
    src_path = Path(src)
    out_file = OUT_DIR / f"{src_path.stem}.docx"

    cv = Converter(str(src_path))
    try:
        cv.convert(str(out_file), start=0, end=None)
    finally:
        cv.close()

    return str(out_file)