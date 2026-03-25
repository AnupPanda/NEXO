from pathlib import Path
from PIL import Image
from app.config import OUT_DIR


def merge_images_to_pdf(paths: list[str], out_name: str = "merged_images.pdf") -> str:
    images = []

    for path in paths:
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)

    if not images:
        raise Exception("No images found to merge.")

    out_file = OUT_DIR / out_name
    first, rest = images[0], images[1:]
    first.save(out_file, save_all=True, append_images=rest)

    return str(out_file)