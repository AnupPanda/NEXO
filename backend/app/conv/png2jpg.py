from pathlib import Path
from PIL import Image
from app.config import OUT_DIR


def png_to_jpg(src: str) -> str:
    src_path = Path(src)
    out_file = OUT_DIR / f"{src_path.stem}.jpg"

    img = Image.open(src_path)
    if img.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[3])
        img = bg
    else:
        img = img.convert("RGB")

    img.save(out_file, "JPEG", quality=95)
    return str(out_file)