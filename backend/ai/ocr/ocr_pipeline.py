import io
import os
import platform
import shutil
import pdfplumber
import pytesseract
from PIL import Image


def _configure_tesseract():
    """
    Configura el path de Tesseract según el sistema operativo.
    - Windows: usa la ruta típica de instalación
    - Linux/Mac/Docker: usa el binario del PATH del sistema
    - Permite override con la variable de entorno TESSERACT_CMD
    """
    env_path = os.environ.get('TESSERACT_CMD')
    if env_path and os.path.exists(env_path):
        pytesseract.pytesseract.tesseract_cmd = env_path
        return

    system = platform.system()

    if system == 'Windows':
        windows_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for p in windows_paths:
            if os.path.exists(p):
                pytesseract.pytesseract.tesseract_cmd = p
                return

    found = shutil.which('tesseract')
    if found:
        pytesseract.pytesseract.tesseract_cmd = found
        return

_configure_tesseract()

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def extract_text_from_image(file_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(file_bytes))
    try:
        text = pytesseract.image_to_string(image, lang='spa+eng')
    except pytesseract.TesseractError:
        try:
            text = pytesseract.image_to_string(image, lang='eng')
        except pytesseract.TesseractError:
            text = pytesseract.image_to_string(image)
    return text.strip()


def extract_text(file_bytes: bytes, filename: str) -> str:
    ext = filename.lower().split(".")[-1]
    if ext == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext in ["jpg", "jpeg", "png"]:
        return extract_text_from_image(file_bytes)
    else:
        raise ValueError(f"Formato no soportado: {ext}")


def _parse_page_range(range_str: str, total_pages: int) -> list[int]:
    """
    Parsea '1-2, 5, 7-9' a una lista de índices (0-based).
    """
    pages = set()
    for part in range_str.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                start, end = part.split('-')
                start = int(start.strip()) - 1
                end = int(end.strip()) - 1
                for p in range(start, end + 1):
                    if 0 <= p < total_pages:
                        pages.add(p)
            except ValueError:
                continue
        else:
            try:
                p = int(part) - 1
                if 0 <= p < total_pages:
                    pages.add(p)
            except ValueError:
                continue
    return sorted(pages)


def extract_text_from_pdf_range(file_bytes: bytes, page_range: str) -> str:
    """Extrae texto solo de las páginas especificadas."""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        pages_to_extract = _parse_page_range(page_range, len(pdf.pages))
        if not pages_to_extract:
            pages_to_extract = list(range(len(pdf.pages)))

        for idx in pages_to_extract:
            page_text = pdf.pages[idx].extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()