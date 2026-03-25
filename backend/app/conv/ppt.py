import subprocess
from pathlib import Path
from app.config import OUT_DIR

def convert_ppt_to_pdf(src: str) -> str:
    src_path = Path(src)
    soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

    cmd = [
        soffice_path, "--headless", "--convert-to", "pdf",
        "--outdir", str(OUT_DIR), str(src_path),
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except Exception as e:
        raise Exception(f"PPT to PDF conversion failed: {str(e)}")

    out_file = OUT_DIR / f"{src_path.stem}.pdf"
    if not out_file.exists():
        raise Exception("PDF creation failed.")
    
    return str(out_file)