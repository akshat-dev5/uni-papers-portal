import os
import json
import logging
import re

# We import your exact OCR engine from Stage 4!
from stage4_ocr import extract_text_from_image

# 1. SETUP LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def count_questions(ocr_data):
    """
    Heuristic to count questions by looking for question marks 
    or standard numbering formats (e.g., '1.', '2)', 'Q3').
    """
    count = 0
    question_pattern = re.compile(r'(^\d+[\.\)]|^[Qq]\.?\s*\d+|\?)')
    for item in ocr_data:
        if question_pattern.search(item['text']):
            count += 1
    return count

def validate_damage(original_ocr_path, clean_image_path, tolerance=0.05):
    """
    Compares the original OCR data against a fresh OCR scan of the cleaned image.
    If the data loss exceeds the tolerance (default 5%), it flags a FAILURE.
    """
    # 1. Load Original Data
    if not os.path.exists(original_ocr_path):
        logging.error(f"Missing original OCR file: {original_ocr_path}")
        return None
        
    with open(original_ocr_path, 'r', encoding='utf-8') as f:
        orig_data = json.load(f)

    # 2. Run Fresh OCR on the Cleaned Image
    logging.info(f"Scanning cleaned image for validation: {os.path.basename(clean_image_path)}")
    clean_data = extract_text_from_image(clean_image_path)
    
    if clean_data is None:
        clean_data = []

    # 3. Calculate Metrics
    orig_words = len(orig_data)
    clean_words = len(clean_data)
    
    orig_chars = sum(len(item['text']) for item in orig_data)
    clean_chars = sum(len(item['text']) for item in clean_data)
    
    orig_qs = count_questions(orig_data)
    clean_qs = count_questions(clean_data)

    # 4. Determine Loss Percentages
    # Prevent division by zero
    word_retention = (clean_words / orig_words) if orig_words > 0 else 1.0
    char_retention = (clean_chars / orig_chars) if orig_chars > 0 else 1.0
    
    # 5. Apply Decision Tree
    # If we lost more than 5% of our characters or words, or lost ANY questions
    failed = False
    failure_reasons = []
    
    if word_retention < (1.0 - tolerance):
        failed = True
        failure_reasons.append(f"Word loss exceeded {tolerance*100}%.")
    if char_retention < (1.0 - tolerance):
        failed = True
        failure_reasons.append(f"Character loss exceeded {tolerance*100}%.")
    if clean_qs < orig_qs:
        failed = True
        failure_reasons.append(f"Lost {orig_qs - clean_qs} question identifiers.")

    status = "FAIL" if failed else "PASS"

    return {
        "status": status,
        "reasons": failure_reasons,
        "metrics": {
            "original": {"words": orig_words, "chars": orig_chars, "questions": orig_qs},
            "cleaned": {"words": clean_words, "chars": clean_chars, "questions": clean_qs},
            "retention": {
                "words": f"{round(word_retention * 100, 2)}%",
                "chars": f"{round(char_retention * 100, 2)}%"
            }
        }
    }

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    base_folder = "decomposed_docs"
    
    print("Starting Stage 10: Automated QA & Damage Detection...\n")
    
    if not os.path.exists(base_folder):
        print(f" Folder '{base_folder}' not found.")
    else:
        doc_folders = [f for f in os.listdir(base_folder) if f.startswith("doc_")]
        
        total_pages = 0
        total_passed = 0
        total_failed = 0
        
        for doc_folder in doc_folders:
            full_doc_path = os.path.join(base_folder, doc_folder)
            clean_dir = os.path.join(full_doc_path, "cleaned_images")
            
            if not os.path.exists(clean_dir):
                continue
                
            clean_images = [p for p in os.listdir(clean_dir) if p.endswith("_clean.png")]
            
            for clean_img in clean_images:
                # Map back to the original OCR file name
                base_name = clean_img.replace("_clean.png", "")
                orig_ocr_file = os.path.join(full_doc_path, f"{base_name}_ocr.json")
                clean_img_path = os.path.join(clean_dir, clean_img)
                report_path = os.path.join(clean_dir, f"{base_name}_qa_report.json")
                
                report = validate_damage(orig_ocr_file, clean_img_path, tolerance=0.05)
                
                if report:
                    total_pages += 1
                    if "PASS" in report["status"]:
                        total_passed += 1
                    else:
                        total_failed += 1
                        
                    # Save the QA report
                    with open(report_path, 'w', encoding='utf-8') as f:
                        json.dump(report, f, indent=4)
                        
                    print(f"[{report['status']}] {doc_folder}/{base_name}")
                    if "FAIL" in report["status"]:
                        for reason in report["reasons"]:
                            print(f"    -> {reason}")

        print("="*40)
        print(" QA COMPLETION REPORT ")
        print("="*40)
        print(f"Total Pages Checked: {total_pages}")
        print(f"Passed (Clean):      {total_passed}")
        print(f"Failed (Damaged):    {total_failed}")
        print("="*40)