import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile
from app.config import UP_DIR


def safe_name(name: str) -> str:
    ext = Path(name).suffix.lower()
    stem = Path(name).stem.replace(" ", "_")
    return f"{stem}_{uuid.uuid4().hex[:8]}{ext}"


def save_upload(file: UploadFile) -> str:
    filename = safe_name(file.filename)
    dest = UP_DIR / filename

    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(dest)