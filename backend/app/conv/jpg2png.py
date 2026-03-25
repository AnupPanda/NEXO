from pathlib import Path
from PIL import Image
from app.config import OUT_DIR


def jpg_to_png(src: str) -> str:
    src_path = Path(src)
    out_file = OUT_DIR / f"{src_path.stem}.png"

    img = Image.open(src_path)
    img.save(out_file, "PNG")

    return str(out_file)