import subprocess
import shutil
from pathlib import Path
from app.config import OUT_DIR

def convert_ppt_to_pdf(src: str) -> str:
    src_path = Path(src)
    
    # --- SMART PATH LOGIC ---
    # Detects the Linux path on Render automatically
    soffice_path = shutil.which("libreoffice") or shutil.which("soffice")

    # Fallback to your specific Windows path for VS Code testing
    if not soffice_path:
        soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

    cmd = [
        str(soffice_path), 
        "--headless", 
        "--convert-to", "pdf",
        "--outdir", str(OUT_DIR), 
        str(src_path),
    ]

    try:
        # Added a 60s timeout since PPTs with many images can take longer to process
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
    except Exception as e:
        raise Exception(f"PPT to PDF conversion failed: {str(e)}")

    out_file = OUT_DIR / f"{src_path.stem}.pdf"
    
    if not out_file.exists():
        raise Exception("PDF creation failed. LibreOffice did not generate the output file.")
    
    return str(out_file)