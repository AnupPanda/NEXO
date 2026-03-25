import subprocess
import shutil
from pathlib import Path
from app.config import OUT_DIR

def convert_excel_to_pdf(src: str) -> str:
    src_path = Path(src)
    
    # --- SMART PATH LOGIC ---
    # Try to find 'libreoffice' or 'soffice' in System Path (Works for Render/Linux)
    soffice_path = shutil.which("libreoffice") or shutil.which("soffice")

    # If not found in system path, fallback to your Windows path (Works for VS Code)
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
        # Run the command with a 30s timeout to prevent hanging on large sheets
        subprocess.run(cmd, check=True, capture_output=True, timeout=30)
    except Exception as e:
        raise Exception(f"Excel to PDF conversion failed: {str(e)}")

    out_file = OUT_DIR / f"{src_path.stem}.pdf"
    
    if not out_file.exists():
        raise Exception("PDF creation failed. The file was not generated.")
        
    return str(out_file)