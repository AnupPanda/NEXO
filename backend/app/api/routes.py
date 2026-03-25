from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse

from app.config import OUT_DIR
from app.util.files import save_upload
from app.util.valid import validate_single, validate_multi
from app.util.clean import remove_file
from app.util.help import out_name

# Original Imports
from app.conv.doc2pdf import convert_docx_to_pdf
from app.conv.pdf2doc import convert_pdf_to_docx
from app.conv.img2pdf import image_to_pdf
from app.conv.pdf2img import pdf_to_image
from app.conv.jpg2png import jpg_to_png
from app.conv.png2jpg import png_to_jpg
from app.conv.mergepdf import merge_images_to_pdf

# NEW Separate Feature Imports
from app.conv.excel import convert_excel_to_pdf
from app.conv.ppt import convert_ppt_to_pdf
from app.conv.mergepdf_tool import merge_pdfs
from app.conv.splitpdf import split_pdf
from app.conv.compress import compress_pdf

router = APIRouter()


@router.get("/")
async def root():
    return {"msg": "NEXO API running"}


@router.post("/convert")
async def convert(
    mode: str = Form(...),
    file: UploadFile | None = File(default=None),
    files: list[UploadFile] | None = File(default=None),
):
    saved_paths = []

    try:
        # 1. HANDLE MULTI-FILE MODES
        if mode in ["merge_images_to_pdf", "merge_pdfs"]:
            validate_multi(files, mode)
            for f in files:
                saved_paths.append(save_upload(f))
            
            if mode == "merge_images_to_pdf":
                out_path = merge_images_to_pdf(saved_paths)
            else:
                out_path = merge_pdfs(saved_paths)

        # 2. HANDLE SINGLE-FILE MODES
        else:
            validate_single(file, mode)
            src = save_upload(file)
            saved_paths.append(src)

            if mode == "docx_to_pdf":
                out_path = convert_docx_to_pdf(src)
            elif mode == "pdf_to_docx":
                out_path = convert_pdf_to_docx(src)
            elif mode == "jpg_to_pdf" or mode == "png_to_pdf":
                out_path = image_to_pdf(src)
            elif mode == "pdf_to_jpg":
                out_path = pdf_to_image(src, "jpg")
            elif mode == "pdf_to_png":
                out_path = pdf_to_image(src, "png")
            elif mode == "jpg_to_png":
                out_path = jpg_to_png(src)
            elif mode == "png_to_jpg":
                out_path = png_to_jpg(src)
            
            # NEW Separate Features Logic
            elif mode == "excel_to_pdf":
                out_path = convert_excel_to_pdf(src)
            elif mode == "ppt_to_pdf":
                out_path = convert_ppt_to_pdf(src)
            elif mode == "split_pdf":
                out_path = split_pdf(src)
            elif mode == "compress_pdf":
                out_path = compress_pdf(src)
            
            else:
                raise Exception("Invalid conversion mode.")

        return JSONResponse({
            "ok": True,
            "msg": "Conversion completed successfully.",
            "file": out_name(out_path),
            "url": f"/download/{out_name(out_path)}"
        })

    except Exception as e:
        return JSONResponse({
            "ok": False,
            "msg": str(e)
        }, status_code=400)

    finally:
        for p in saved_paths:
            remove_file(p)


@router.get("/download/{name}")
async def download(name: str):
    file_path = OUT_DIR / name
    if not file_path.exists():
        return JSONResponse({"ok": False, "msg": "File not found."}, status_code=404)

    return FileResponse(
        path=str(file_path),
        filename=name,
        media_type="application/octet-stream"
    )