import subprocess
import os
import shutil
from pathlib import Path
from app.config import OUT_DIR

def convert_docx_to_pdf(src: str) -> str:
    src_path = Path(src)
    out_dir = OUT_DIR

    # --- SMART PATH LOGIC ---
    # 1. Try to find 'libreoffice' or 'soffice' in the System Path (Works for Render/Linux)
    soffice_path = shutil.which("libreoffice") or shutil.which("soffice")

    # 2. If not found in system path, fallback to your Windows path (Works for VS Code)
    if not soffice_path:
        soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

    cmd = [
        str(soffice_path),
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(out_dir),
        str(src_path),
    ]

    try:
        # Run the command
        subprocess.run(cmd, check=True, capture_output=True)
    except Exception as e:
        # Provide a clearer error message for debugging
        raise Exception(f"Conversion Engine Error: {str(e)}")

    # Check for the resulting PDF
    out_file = out_dir / f"{src_path.stem}.pdf"

    if not out_file.exists():
        raise Exception(f"PDF creation failed. Check if {src_path.name} is valid.")

    return str(out_file)