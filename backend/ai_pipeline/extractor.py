import re
import os
from diagram_extractor import detect_and_save_diagrams
def parse_confidence_score(raw_text):
    matches = re.findall(r'(\d+)%', raw_text)
    return int(matches[-1]) if matches else None

def structure_output(raw_text, pdf_filename, page_number, image, output_images_dir):
    os.makedirs(output_images_dir, exist_ok=True)
    
    diagram_paths = detect_and_save_diagrams(image, pdf_filename, page_number, output_images_dir)

    return {
        "source_file": pdf_filename,
        "page_number": page_number,
        "extracted_content": raw_text,
        "diagrams": diagram_paths,
        "confidence_score": parse_confidence_score(raw_text)
    }

def combine_pages(pages_output):
    valid_scores = [p["confidence_score"] for p in pages_output if p.get("confidence_score") is not None]
    overall_confidence = round(sum(valid_scores) / len(valid_scores)) if valid_scores else None
    
    return {
        "source_file": pages_output[0]["source_file"],
        "total_pages": len(pages_output),
        "pages": pages_output,
        "overall_confidence": overall_confidence
    }