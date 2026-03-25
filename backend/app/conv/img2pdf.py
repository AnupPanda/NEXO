from pathlib import Path
from PIL import Image
from app.config import OUT_DIR


def image_to_pdf(src: str) -> str:
    src_path = Path(src)
    out_file = OUT_DIR / f"{src_path.stem}.pdf"

    img = Image.open(src_path)
    if img.mode != "RGB":
        img = img.convert("RGB")

    img.save(out_file, "PDF", resolution=100.0)
    return str(out_file)