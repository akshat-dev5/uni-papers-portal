from pdf2image import convert_from_path
from config import DPI
import os

# Try to get POPPLER_PATH from environment variable first
POPPLER_PATH = os.getenv("POPPLER_PATH")
if not POPPLER_PATH:
    POPPLER_PATH = r"D:\MUQP_Internship\poppler-25.12.0\Library\bin"

def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path, dpi=DPI, poppler_path=POPPLER_PATH)
    return images