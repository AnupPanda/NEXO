import subprocess
from pathlib import Path
from app.config import OUT_DIR


def convert_docx_to_pdf(src: str) -> str:
    src_path = Path(src)
    out_dir = OUT_DIR

    # Full path to LibreOffice
    soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

    cmd = [
        soffice_path,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(out_dir),
        str(src_path),
    ]

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True
        )
    except FileNotFoundError:
        raise Exception("LibreOffice not found. Check installation path.")
    except subprocess.CalledProcessError as e:
        raise Exception(
            f"DOCX to PDF conversion failed:\n{e.stderr.decode(errors='ignore')}"
        )

    out_file = out_dir / f"{src_path.stem}.pdf"

    if not out_file.exists():
        raise Exception("PDF file was not created.")

    return str(out_file)