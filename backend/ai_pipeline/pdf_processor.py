from pdf2image import convert_from_path
from config import DPI

import os

def pdf_to_images(pdf_path):
    POPPLER_PATH = os.getenv("POPPLER_PATH", r"D:\MUQP_Internship\poppler-25.12.0\Library\bin")
    
    print(f"Using Poppler from: {POPPLER_PATH}")
    images = convert_from_path(pdf_path, dpi=DPI, poppler_path=POPPLER_PATH)
    return images