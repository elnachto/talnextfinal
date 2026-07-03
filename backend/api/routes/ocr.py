from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ai.ocr.ocr_pipeline import extract_text, extract_text_from_pdf_range
import traceback

router = APIRouter()


@router.post("/extract-text")
async def extract_text_from_file(
    file: UploadFile = File(...),
    page_range: str = Form(default=""),
):
    allowed = ["pdf", "jpg", "jpeg", "png"]
    ext = file.filename.lower().split(".")[-1]

    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Formato no soportado")

    file_bytes = await file.read()

    try:
        if ext == "pdf" and page_range.strip():
            text = extract_text_from_pdf_range(file_bytes, page_range.strip())
        else:
            text = extract_text(file_bytes, file.filename)

        return {
            "filename": file.filename,
            "characters": len(text),
            "text": text,
        }
    except Exception as e:
        # Odio los errores
        print("=" * 60)
        print(f"ERROR EN /extract-text con archivo: {file.filename}")
        print(f"Tipo error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        print("=" * 60)
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")