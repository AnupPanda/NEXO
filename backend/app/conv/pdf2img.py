from pathlib import Path
import fitz
from app.config import OUT_DIR


def pdf_to_image(src: str, fmt: str = "png") -> str:
    src_path = Path(src)
    doc = fitz.open(str(src_path))

    if len(doc) == 0:
        raise Exception("PDF has no pages.")

    page = doc.load_page(0)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

    out_file = OUT_DIR / f"{src_path.stem}.{fmt}"
    pix.save(str(out_file))
    doc.close()

    return str(out_file)