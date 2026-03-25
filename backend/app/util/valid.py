from fastapi import UploadFile, HTTPException

# This dictionary MUST include the new modes
ALLOWED_EXTS = {
    "docx_to_pdf": [".docx"],
    "pdf_to_docx": [".pdf"],
    "jpg_to_pdf": [".jpg", ".jpeg"],
    "png_to_pdf": [".png"],
    "pdf_to_jpg": [".pdf"],
    "pdf_to_png": [".pdf"],
    "jpg_to_png": [".jpg", ".jpeg"],
    "png_to_jpg": [".png"],
    "merge_images_to_pdf": [".jpg", ".jpeg", ".png"],
    # ADD THESE NEW ONES:
    "merge_pdfs": [".pdf"],
    "split_pdf": [".pdf"],
    "compress_pdf": [".pdf"],
    "ppt_to_pdf": [".ppt", ".pptx"],
    "excel_to_pdf": [".xls", ".xlsx"]
}

def validate_single(file: UploadFile, mode: str):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    
    ext = "." + file.filename.split(".")[-1].lower()
    if mode not in ALLOWED_EXTS or ext not in ALLOWED_EXTS[mode]:
        allowed = ", ".join(ALLOWED_EXTS.get(mode, []))
        raise HTTPException(status_code=400, detail=f"Invalid file type for {mode}. Allowed: {allowed}")

def validate_multi(files: list[UploadFile], mode: str):
    if not files or len(files) < 2:
        raise HTTPException(status_code=400, detail="Please upload at least 2 files.")
    
    for f in files:
        ext = "." + f.filename.split(".")[-1].lower()
        if mode not in ALLOWED_EXTS or ext not in ALLOWED_EXTS[mode]:
            raise HTTPException(status_code=400, detail=f"File {f.filename} is not supported for {mode}.")