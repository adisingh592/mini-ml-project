"""
HexaDisease - Multi-Format Medical Report Reader
Extracts text from PDF reports, image scans (OCR), and plain text documents.
"""

import json
import os

TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".log"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}

class ReportReadError(Exception):
    pass

def read_pdf(path):
    # Try fitz (PyMuPDF) first - fastest and most reliable
    try:
        import fitz
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc).strip()
        if text:
            return text
    except Exception:
        pass

    # Try pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages).strip()
        if text:
            return text
    except Exception:
        pass

    # Try pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
            text = "\n".join(pages).strip()
            if text:
                return text
    except Exception:
        pass

    raise ReportReadError(
        "Could not extract digital text from this PDF. If it is a scanned document, "
        "save it as an image (PNG/JPG) for OCR processing."
    )

def read_image(path):
    try:
        import pytesseract
        from PIL import Image
        return pytesseract.image_to_string(Image.open(path))
    except ImportError:
        raise ReportReadError("Image OCR requires pytesseract and pillow.")
    except Exception as e:
        raise ReportReadError(f"OCR reading failed: {e}")

def read_report(path):
    if not os.path.exists(path):
        raise ReportReadError(f"Report file not found: {path}")

    ext = os.path.splitext(path)[1].lower()

    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return "", json.load(f)
    if ext == ".pdf":
        return read_pdf(path), None
    if ext in IMAGE_EXTENSIONS:
        return read_image(path), None
    if ext in TEXT_EXTENSIONS or ext == "":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(), None

    raise ReportReadError(f"Unsupported report format '{ext}'. Supported: .pdf, .txt, .json, .png, .jpg")
