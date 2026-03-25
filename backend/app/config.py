from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"

UP_DIR = BASE_DIR / "up"
OUT_DIR = BASE_DIR / "out"
TMP_DIR = BASE_DIR / "tmp"

MAX_MULTI_FILES = 20

CONVERT_MAP = {
    "docx_to_pdf": [".docx"],
    "pdf_to_docx": [".pdf"],
    "jpg_to_pdf": [".jpg", ".jpeg"],
    "png_to_pdf": [".png"],
    "pdf_to_jpg": [".pdf"],
    "pdf_to_png": [".pdf"],
    "jpg_to_png": [".jpg", ".jpeg"],
    "png_to_jpg": [".png"],
    "merge_images_to_pdf": [".jpg", ".jpeg", ".png"],
}